#!/usr/bin/env bash
#
# Behavioral regression tests for ask-first-guard.sh.
#
# Asserts the truth table that prose alone cannot guarantee: the always-ask floor
# is unconditional (no env knob disables it), PR/deploy follow traffic state and the
# ASSEMBLY_ASK_FIRST_PR/_DEPLOY overrides, and the rm -rf carve-out passes temp /
# project-relative deletes while still asking on anything dangerous.
#
# Exit 0 = all pass. Requires bash + python3 (same as the guard's fallback parser).

set -uo pipefail

# Start from a clean slate even if the caller's shell exports these.
unset ASSEMBLY_ASK_FIRST ASSEMBLY_ASK_FIRST_PR ASSEMBLY_ASK_FIRST_DEPLOY \
      ASSEMBLY_ASK_FIRST_PUSH ASSEMBLY_ASK_FIRST_BRANCH ASSEMBLY_ASK_FIRST_DESTRUCTIVE 2>/dev/null || true

HERE="$(cd "$(dirname "$0")" && pwd)"
GUARD="$HERE/ask-first-guard.sh"
fails=0; total=0

payload() { python3 -c 'import json,sys; print(json.dumps({"tool_name":"Bash","tool_input":{"command":sys.argv[1]}}))' "$1"; }

# expect EXPECT(ask|pass) PROJDIR ENV(space-sep VAR=val, or "") CMD
expect() {
  local exp="$1" proj="$2" envs="$3" cmd="$4" out got
  total=$((total + 1))
  out="$(payload "$cmd" | env CLAUDE_PROJECT_DIR="$proj" $envs bash "$GUARD" 2>/dev/null)"
  got=pass; [ -n "$out" ] && got=ask
  if [ "$got" != "$exp" ]; then
    fails=$((fails + 1))
    printf 'FAIL  want=%-4s got=%-4s env=[%s] cmd=%s\n' "$exp" "$got" "$envs" "$cmd"
  fi
}

mk() { local d; d="$(mktemp -d)"; if [ -n "${2:-}" ]; then mkdir -p "$d/$(dirname "$2")"; printf 'Traffic state: %s\n' "$1" >"$d/$2"; fi; printf '%s' "$d"; }

NONE="$(mktemp -d)"                                   # no status file -> pre-live
PRELIVE="$(mk pre-live .agents/status.md)"
LIVE="$(mk live .agents/status.md)"
LIVEDOCS="$(mk live docs/status.md)"                  # legacy fallback path
LIVECRLF="$(mktemp -d)"; mkdir -p "$LIVECRLF/.agents"; printf 'Traffic state: live\r\n' >"$LIVECRLF/.agents/status.md"

# --- pre-live: PR + deploy autonomous; floor still asks ---
for P in "$NONE" "$PRELIVE"; do
  expect pass "$P" "" 'gh pr create -t x -b y'
  expect pass "$P" "" 'gh pr merge 12 --squash'
  expect pass "$P" "" 'gh pr ready 12'
  expect pass "$P" "" 'wrangler deploy'
  expect pass "$P" "" 'npm publish'
  expect pass "$P" "" 'gh release create v1.0.0'
  expect pass "$P" "" 'vercel --prod'
done
expect ask "$NONE" "" 'git push --force origin topic'
expect ask "$NONE" "" 'git push origin main'
expect ask "$NONE" "" 'git branch -D old'
expect ask "$NONE" "" 'git reset --hard HEAD~1'
expect ask "$NONE" "" 'terraform apply'
expect ask "$NONE" "" 'kubectl delete pod x'
expect ask "$NONE" "" 'aws s3 rm s3://bucket --recursive'
expect ask "$NONE" "" 'dd if=/dev/zero of=/dev/disk2'
expect ask "$NONE" "" 'mkfs.ext4 /dev/sdb'

# --- live: create/ready autonomous, merge + deploy ask ---
expect pass "$LIVE" "" 'gh pr create -t x'
expect pass "$LIVE" "" 'gh pr ready 12'
expect ask  "$LIVE" "" 'gh pr merge 12'
expect ask  "$LIVE" "" 'gh api -X PUT repos/o/r/pulls/12/merge'
expect ask  "$LIVE" "" 'wrangler deploy'
expect ask  "$LIVE" "" 'gh release create v1'
expect ask  "$LIVE" "" 'npm publish'

# --- CRLF and legacy docs/status.md both detect live ---
expect ask "$LIVECRLF" "" 'gh pr merge 12'
expect ask "$LIVECRLF" "" 'wrangler deploy'
expect ask "$LIVEDOCS" "" 'gh pr merge 12'

# --- env overrides beat traffic state (for the tunable classes only) ---
expect pass "$LIVE"    "ASSEMBLY_ASK_FIRST_PR=off"     'gh pr merge 12'
expect ask  "$PRELIVE" "ASSEMBLY_ASK_FIRST_DEPLOY=on"  'wrangler deploy'
expect ask  "$LIVE"    "ASSEMBLY_ASK_FIRST_PR=on"      'gh pr create -t x'

# --- floor is LOCKED: retired/unknown knobs cannot disable it ---
expect ask "$NONE" "ASSEMBLY_ASK_FIRST=off"             'rm -rf /etc/nginx'
expect ask "$NONE" "ASSEMBLY_ASK_FIRST_DESTRUCTIVE=off" 'rm -rf /etc/nginx'
expect ask "$NONE" "ASSEMBLY_ASK_FIRST_DESTRUCTIVE=off" 'dd if=/dev/zero of=/dev/disk2'
expect ask "$NONE" "ASSEMBLY_ASK_FIRST_PUSH=off"        'git push --force origin main'
expect ask "$NONE" "ASSEMBLY_ASK_FIRST_BRANCH=off"      'git branch -D x'
expect ask "$NONE" "ASSEMBLY_ASK_FIRST=off"             'terraform destroy'

# --- rm -rf carve-out: temp + project-relative pass ---
expect pass "$NONE" "" 'rm -rf /tmp/hcs-check'
expect pass "$NONE" "" 'rm -rf /private/tmp/x'
expect pass "$NONE" "" 'rm -rf /var/folders/ab/cd/T/zz'
expect pass "$NONE" "" 'rm -rf node_modules'
expect pass "$NONE" "" 'rm -rf ./build dist .next'
expect pass "$NONE" "" 'rm -rf "$TMPDIR/build"'
expect pass "$NONE" "" 'rm -rf /tmp/hcs-check && git clone --quiet https://github.com/x/y /tmp/hcs-check'

# --- rm -rf carve-out: dangerous targets still ask ---
expect ask "$NONE" "" 'rm -rf /'
expect ask "$NONE" "" 'rm -rf /etc'
expect ask "$NONE" "" 'rm -rf /Users/sai/project'
expect ask "$NONE" "" 'rm -rf ~'
expect ask "$NONE" "" 'rm -rf ~/Library'
expect ask "$NONE" "" 'rm -rf "$HOME/x"'
expect ask "$NONE" "" 'rm -rf $DIR'
expect ask "$NONE" "" 'rm -rf *'
expect ask "$NONE" "" 'rm -rf /tmp/*'
expect ask "$NONE" "" 'rm -rf ../sibling'
expect ask "$NONE" "" 'rm -rf .'
expect ask "$NONE" "" 'rm -rf "/etc/nginx"'
expect ask "$NONE" "" 'rm -rf /tmp/ok /etc/bad'

# --- benign commands always pass ---
expect pass "$NONE" "" 'git push origin feature'
expect pass "$NONE" "" 'gh pr create --draft -t x'
expect pass "$NONE" "" 'npm install'
expect pass "$NONE" "" 'git restore --staged .'
expect pass "$NONE" "" 'git clean -n'
expect pass "$NONE" "" 'echo add things and build'

rm -rf "$NONE" "$PRELIVE" "$LIVE" "$LIVEDOCS" "$LIVECRLF"

if [ "$fails" -eq 0 ]; then
  printf 'OK: ask-first-guard %d/%d cases passed\n' "$total" "$total"
  exit 0
fi
printf 'FAILED: %d/%d cases failed\n' "$fails" "$total"
exit 1
