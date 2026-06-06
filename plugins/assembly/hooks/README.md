# Hooks

Plugin-level hooks that Claude Code loads from `hooks/hooks.json` when Assembly is
enabled. **Claude Code only** — Codex does not read this directory, so these hooks
are additive enhancements that degrade to nothing on the Codex runtime. The shared
`skills/` surface is identical in both.

These ship intentionally small, read-only or ask-only, and dependency-light. They
never modify files and never block a tool call on a missing dependency.

## Contents

- SessionStart primer
- Ask-first guard
- Design constraints
- Opting out

## SessionStart primer — `session-start.sh`

Runs when a session starts or resumes. If the working directory is an Assembly
project (it has `.agents/status.md`), it injects a short orientation into the
session: read `.agents/status.md` first, the current phase, the skills `status.md`
recommends next, the lifecycle spine, and the ask-first floor. If there is no
`.agents/status.md`, it emits nothing and exits 0, so non-Assembly projects are
unaffected.

This operationalizes the project convention that *agents get one obvious place to
start: `.agents/status.md`* — instead of relying on the user to remember to invoke a
skill at the top of every session.

## Ask-first guard — `ask-first-guard.sh`

A `PreToolUse` hook on the `Bash` tool. When a command looks like one of the
ask-first-floor actions, it returns `permissionDecision: "ask"` with a reason, so
the human confirms even when the project runs under `bypassPermissions`. It is the
runtime counterpart to the prose floor in [`docs/SPEC.md`](../docs/SPEC.md): the
scaffold grants maximum default permissions for speed, and this guard re-introduces
friction **only** at the irreversible boundaries.

It re-prompts on:

| Class | Examples (incl. flag-split, long-form, and refspec variants) |
| --- | --- |
| PR merge / ready / non-draft create / release | `gh pr merge`, `gh api …/pulls/N/merge`, `gh pr ready`, `gh pr create` (without `--draft`), `gh release create` |
| Force / main / delete pushes | `git push --force` / `--force-with-lease` / `--mirror` / `+main`, `git push … main` / `HEAD:main`, `git push --delete`, including with `git -C <path>` / `git -c …` prefixes |
| Branch, history & working-tree destruction | `git branch -D` / `--delete`, `git reset --hard`, `git clean -f…` / `--force`, `git checkout .`, `git restore .` |
| Deploy / publish | `wrangler deploy` / `wrangler pages deploy`, `vercel … --prod`, `netlify deploy`, `npm/pnpm/yarn/bun publish` |
| Infrastructure / catastrophic | `terraform apply/destroy`, `kubectl delete`, `aws s3 rm --recursive`, `dd`, `mkfs`, `rm -rf` (any flag order) |

Anything else passes through untouched (a normal `git push` of a topic branch, a
`git restore --staged`, a `git clean -n` dry run, `gh pr create --draft`, and
`npm install`/`run` are not flagged — those are routine).

**Limits.** It matches a flat command string, so it is defense in depth, not a
sandbox. It cannot see:

- Actions behind shell **aliases** or **script wrappers** (`npm run deploy`,
  `make ship`) — the dangerous verb is hidden from the matcher.
- A push to a protected branch when that branch is the **current checkout**
  (`git push` with no explicit ref).
- **Money, credential, or external-messaging** actions that are not shell commands
  — those stay governed by the protocol and Claude Code's own tool-level prompts.

It fails **closed** (asks) if it cannot evaluate a command, and biases toward
asking, so it may occasionally ask about a benign command — a single keystroke
approves. Extend the command classes by editing `ask-first-guard.sh`.

## Design constraints

- **No file mutation.** Both hooks are read-only / ask-only.
- **Graceful degradation.** The guard prefers `jq`, falls back to `python3`, and
  finally scans the raw payload; it never blocks a tool call because a tool is
  missing.
- **Cross-platform.** Plain `bash` + POSIX text tools. On Windows these run under
  Git Bash, the same as other plugin command hooks.
- **`${CLAUDE_PLUGIN_ROOT}`** resolves to this bundle so the hook commands find
  these scripts regardless of where the plugin is installed.

## Opting out

Plugin hooks run once the plugin is enabled. To disable them, disable the Assembly
plugin, or remove an entry from `hooks/hooks.json` in your local cache. To tune the
guard's command classes, edit `ask-first-guard.sh`.
