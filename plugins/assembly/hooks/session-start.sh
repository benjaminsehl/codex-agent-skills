#!/usr/bin/env bash
#
# Assembly SessionStart hook (Claude Code only).
#
# Orients each new session to the project's paper trail: points the agent at
# .agents/status.md, surfaces the current phase and recommended next skills, and
# restates the ask-first floor. Stays completely silent (exit 0, no output) when
# this is not an Assembly project, so it never interferes elsewhere.
#
# Reads nothing from stdin and depends only on POSIX text tools, so it degrades
# gracefully if jq is missing.

set -euo pipefail

project_dir="${CLAUDE_PROJECT_DIR:-$PWD}"
status_file="$project_dir/.agents/status.md"

# No root project workspace -> not an Assembly project -> say nothing.
[ -f "$status_file" ] || exit 0

# Current phase, e.g. the line "Current phase: build".
phase_line="$(grep -m1 -iE '^current phase:' "$status_file" 2>/dev/null || true)"
phase="$(printf '%s' "${phase_line#*:}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"

# Skills listed under "## Next Recommended Skills" (backtick-wrapped tokens).
next_skills="$(awk '/^## Next Recommended Skills/{f=1;next} /^## /{f=0} f' "$status_file" 2>/dev/null \
  | grep -oE '`[a-z][a-z-]*`' 2>/dev/null \
  | tr -d '`' \
  | paste -sd, - 2>/dev/null \
  | sed 's/,/, /g' || true)"

printf 'Assembly is active in this project.\n'
printf -- '- Orientation: read .agents/status.md first; it holds current project state and evidence.\n'
[ -n "$phase" ] && printf -- '- Current phase (per .agents/status.md): %s\n' "$phase"
[ -n "$next_skills" ] && printf -- '- status.md recommends next: %s\n' "$next_skills"
printf -- '- Continue with the `next` skill; use `project-status` if the trail looks stale.\n'
printf -- '- Lifecycle spine: spec -> plan -> build -> test -> review -> code-simplify -> ship.\n'
printf -- '- Ask-first floor stays in effect: confirm before merging PRs, deploying, force-pushing, deleting branches, destructive ops, money, credentials, or external messaging.\n'

exit 0
