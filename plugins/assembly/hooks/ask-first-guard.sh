#!/usr/bin/env bash
#
# Assembly ask-first guard (Claude Code only).
#
# A PreToolUse hook on the Bash tool. When a command looks like one of the
# Assembly "ask-first floor" actions, it returns permissionDecision "ask" so the
# human confirms even under bypassPermissions. Otherwise it stays silent (exit 0)
# and the normal permission flow proceeds.
#
# This is the runtime counterpart to the prose floor in docs/SPEC.md. It is
# defense in depth, not a sandbox: it matches a flat command string, so it cannot
# see actions hidden behind shell aliases, script wrappers (`npm run deploy`,
# `make ship`), or a protected branch that is the current checkout. It catches the
# natural command forms an agent emits (including `;`/`&&`/`|`/subshell chaining and
# tab spacing), but a flat matcher cannot defeat deliberate obfuscation — a verb
# built from variables (`rm$IFS-rf`), run through `eval`/`bash -c`, or reached via
# `xargs rm`/`find -delete` will pass; airtight enforcement would need a shell
# parser. It biases toward a one-keystroke confirmation and fails closed (asks) if
# it cannot evaluate. It cannot see money, credential, or external-messaging actions
# that are not shell commands — those stay governed by the protocol and tool-level
# permission prompts.
#
# The PR and deploy classes are tuned per project by the founder's `Traffic state:`
# in .agents/status.md (pre-live runs PRs/merges/deploys autonomously; live gates
# merge-to-default and deploy) and the ASSEMBLY_ASK_FIRST_PR / _DEPLOY environment
# variables (hooks/README.md). The always-ask floor — force/main/delete pushes,
# branch & working-tree destruction, and catastrophic ops — is unconditional. An
# `rm -rf` passes only when every target is a temp or project-relative path; any
# absolute, home, variable, glob, or parent-traversal target still asks.
#
# All reason strings below are interpolated into JSON by raw substitution, so they
# MUST stay free of double quotes, backslashes, and newlines.

set -euo pipefail

payload="$(cat)"

# A safety control must fail closed: if we cannot run our matcher, ask.
if ! command -v grep >/dev/null 2>&1; then
  printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Assembly ask-first guard could not evaluate this command (grep unavailable). Confirm manually."}}'
  exit 0
fi

# Extract the Bash command. Prefer jq, then python3. Only when neither parser is
# present do we scan the raw payload (coarse, but safe-failing toward "ask").
cmd=""
have_parser=0
if command -v jq >/dev/null 2>&1; then
  have_parser=1
  cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null || true)"
elif command -v python3 >/dev/null 2>&1; then
  have_parser=1
  cmd="$(printf '%s' "$payload" | python3 -c 'import json,sys
try:
    print(json.load(sys.stdin).get("tool_input", {}).get("command", ""))
except Exception:
    pass' 2>/dev/null || true)"
fi
[ "$have_parser" -eq 1 ] || cmd="$payload"

# A parser that returned nothing means there is no command to guard.
[ -n "$cmd" ] || exit 0

# has PATTERN -> true when the command matches the extended regex (case-insensitive).
has() { printf '%s' "$cmd" | grep -Eiq -e "$1"; }

# `git` may carry global options before the subcommand (e.g. `git -C <path> push`,
# `git -c push.default=current push`). Allow them so the subcommand matchers still
# fire — `git -C` is the canonical way an agent operates on a repo without `cd`.
GIT='git( +(-c +[^ ]+|-C +[^ ]+|--git-dir(=[^ ]+| +[^ ]+)|--work-tree(=[^ ]+| +[^ ]+)|--namespace(=[^ ]+| +[^ ]+)|-p|--paginate|--no-pager|--bare))*'

# Force flags / refspecs: --force, --force-with-lease, short clusters containing f
# (-f, -fu, -uf), --mirror (can delete every remote branch), and +refspec.
FORCE='(--force([[:space:]]|$)|--force-with-lease|--mirror|[[:space:]]-[a-z]*f[a-z]*([[:space:]]|$)|[[:space:]]\+[A-Za-z])'
# A "main"/"master" target as a bare arg, a :refspec dest, or a +refspec dest.
MAIN='([[:space:]]|:|\+)(refs/heads/)?(main|master)([[:space:]]|$)'

# --- Configuration: traffic state + PR/deploy overrides ------------------------
# Only the PR and deploy classes are tunable. The always-ask floor (force/main/
# delete pushes, branch & working-tree destruction, catastrophic ops) is
# unconditional and cannot be disabled here — matching the SPEC's always-ask floor
# "any traffic state", so a checked-in project setting can never silence it.
#
# Two knobs, value off|0|false|no = never ask, on|1|true|yes = always ask, unset =
# use the traffic-state default. Set globally in ~/.claude/settings.json "env" or
# per project in <project>/.claude/settings.json. See hooks/README.md.
#
#   ASSEMBLY_ASK_FIRST_PR      pull-request create / ready / merge.
#   ASSEMBLY_ASK_FIRST_DEPLOY  deploy / publish / GitHub release.

# env_decision VAR -> "off" | "on" | "" (unset / unrecognized).
env_decision() {
  local var="$1" val
  val="$(printf '%s' "${!var:-}" | tr 'A-Z' 'a-z')"
  case "$val" in
    off|0|false|no) printf off ;;
    on|1|true|yes)  printf on ;;
  esac
}

# Traffic state (founder-set; absent/unknown -> pre-live). Read the canonical
# .agents/status.md, falling back to the legacy docs/status.md — the same source
# the SessionStart primer reads. tr -d strips a trailing CR from CRLF files.
project_dir="${CLAUDE_PROJECT_DIR:-${PWD:-.}}"
traffic="pre-live"
for status_file in "$project_dir/.agents/status.md" "$project_dir/docs/status.md"; do
  [ -f "$status_file" ] || continue
  ts_line="$(grep -m1 -iE '^traffic state:' "$status_file" 2>/dev/null || true)"
  [ -n "$ts_line" ] || continue
  ts_val="$(printf '%s' "${ts_line#*:}" | tr -d '\r' | tr 'A-Z' 'a-z' | awk '{print $1}')"
  if [ "$ts_val" = live ]; then traffic="live"; fi
  break
done

# should_ask VAR DEFAULT -> 0 (ask) / 1 (do not ask). Env override beats DEFAULT.
should_ask() {
  case "$(env_decision "$1")" in
    off) return 1 ;;
    on)  return 0 ;;
  esac
  [ "$2" = ask ]
}

# rm_safe -> 0 when every target of an rm -rf is clearly safe (a temp path, or a
# project-relative path), 1 (ask) otherwise. Fails toward ask on anything uncertain:
# a variable, ~, a glob, parent traversal (..), a bare / or bare . target, or any
# absolute path outside /tmp, /private/tmp, /var/folders (incl. $TMPDIR).
rm_safe() {
  local c tok safe=1
  c="$(printf '%s' "$cmd" | sed -E 's#\$\{?TMPDIR\}?#/tmp#g')"
  c="${c//\"/}"; c="${c//\'/}"   # drop quotes so quoted paths still classify
  # Any metacharacter that can hide or expand a path defeats token classification
  # (e.g. a backslash makes \/etc not start with /), so fail toward ask.
  case "$c" in *'$'*|*'`'*|*'~'*|*'*'*|*'\'*) return 1 ;; esac
  printf '%s' "$c" | grep -Eq '(^| |/)\.\.(/| |$)' && return 1
  set -f
  for tok in $c; do
    case "$tok" in
      /|.|./)                                                  safe=0 ;;
      /tmp|/tmp/*|/private/tmp|/private/tmp/*|/var/folders/*)  : ;;
      /*)                                                      safe=0 ;;
    esac
    [ "$safe" -eq 1 ] || break
  done
  set +f
  [ "$safe" -eq 1 ]
}

# pre-live runs PRs, merges, and deploys autonomously; live re-gates merge-to-
# default and deploy. An env knob (off/on) overrides the traffic-state default.
pr_merge_default=pass; deploy_default=pass
if [ "$traffic" = live ]; then pr_merge_default=ask; deploy_default=ask; fi

should_ask ASSEMBLY_ASK_FIRST_PR     "$pr_merge_default" && ask_pr_merge=1  || ask_pr_merge=0
should_ask ASSEMBLY_ASK_FIRST_PR     pass                && ask_pr_create=1 || ask_pr_create=0
should_ask ASSEMBLY_ASK_FIRST_DEPLOY "$deploy_default"   && ask_deploy=1    || ask_deploy=0

reason=""
# --- Pull requests (tunable: ASSEMBLY_ASK_FIRST_PR / traffic state) -------------
if   [ "$ask_pr_merge"  -eq 1 ] && has 'gh +pr +merge';    then reason="merging a pull request"
elif [ "$ask_pr_merge"  -eq 1 ] && has 'gh +api( |$)' && has 'pulls/[0-9]+/merge'; then reason="merging a pull request via gh api"
elif [ "$ask_pr_create" -eq 1 ] && has 'gh +pr +ready';    then reason="marking a pull request ready for review"
elif [ "$ask_pr_create" -eq 1 ] && has 'gh +pr +create' && ! has '(--draft|-d)( |$)'; then reason="creating a non-draft pull request"
# --- Deploy / publish (tunable: ASSEMBLY_ASK_FIRST_DEPLOY / traffic state) ------
elif [ "$ask_deploy" -eq 1 ] && has 'gh +release +create'; then reason="publishing a GitHub release"
elif [ "$ask_deploy" -eq 1 ] && has '(^| )(wrangler|netlify) +(pages +)?(deploy|publish)'; then reason="deploying"
elif [ "$ask_deploy" -eq 1 ] && has '(^| )wrangler +versions +deploy'; then reason="deploying"
elif [ "$ask_deploy" -eq 1 ] && has '(^| )vercel\b' && has '(--prod|--prebuilt)'; then reason="a production deploy"
elif [ "$ask_deploy" -eq 1 ] && has '(^| )(npm|pnpm|yarn|bun) +publish'; then reason="publishing a package"
# --- Always-ask floor: unconditional in any traffic state ----------------------
# git push family
elif has "${GIT} +push" && has "$FORCE"; then reason="force-pushing or mirroring"
elif has "${GIT} +push" && has '(--delete| :)'; then reason="deleting a remote branch"
elif has "${GIT} +push" && has "$MAIN"; then reason="pushing directly to main/master"
# branch & history destruction
elif has "${GIT} +branch +(-[a-z]*[dD]([[:space:]]|$)|--delete)"; then reason="deleting a branch"
elif has "${GIT} +reset" && has '--hard'; then reason="a hard reset (discards uncommitted work)"
elif has "${GIT} +clean" && has '(--force|-[a-z]*f[a-z]*([[:space:]]|$))'; then reason="git clean (deletes untracked files)"
elif has "${GIT} +checkout +(--[[:space:]]+)?\.([[:space:]]|$)"; then reason="discarding working-tree changes (git checkout .)"
elif has "${GIT} +restore" && has '[[:space:]]\.([[:space:]]|$)' && ! has '\-\-staged'; then reason="discarding working-tree changes (git restore .)"
# infrastructure / catastrophic
elif has 'terraform +(apply|destroy)'; then reason="a terraform apply/destroy"
elif has 'kubectl +delete'; then reason="deleting Kubernetes resources"
elif has '(^|[[:space:]]|[/;&|(){}])aws +s3 +rm' && has '--recursive'; then reason="a recursive S3 delete"
elif has '(^|[[:space:]]|[/;&|(){}])(dd +|mkfs)'; then reason="a raw disk write (dd/mkfs)"
# recursive force delete — passes only when every target is a temp/relative path
elif has '(^|[[:space:]]|[/;&|(){}])rm[[:space:]]' \
     && has '(-[a-z]*r[a-z]*([[:space:]]|$)|--recursive)' \
     && has '(-[a-z]*f[a-z]*([[:space:]]|$)|--force)' \
     && ! rm_safe; then reason="a recursive force delete (rm -rf) outside a temp or project path"
fi

[ -n "$reason" ] || exit 0

msg="Assembly ask-first floor: this command looks like ${reason}. Per the Assembly SPEC, confirm before merging PRs, deploying, force-pushing, deleting branches or refs, publishing, or destructive operations. Approve to proceed, or revise the command."

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"%s"}}\n' "$msg"
exit 0
