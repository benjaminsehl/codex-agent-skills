# Project Lifecycle Workflow

## Contents

- Start or scaffold
- Status orientation
- Repair and introspection
- Retro and learning

Use this reference from `init`, `project-status`, and `next`. It keeps project-control behavior behind a small public gateway so users do not need to remember separate `new-project`, `introspect`, `retro`, or `learn` commands.

## Start Or Scaffold

Owned by the `init` skill. `project-status` and `next` route to `init` when project docs are missing.

Use this mode when project docs are missing, the user is restarting a project, or the user asks to start a new project, subproject, or substantial project slice.

- Default roots: `.agents/` (operational trail) and `docs/` (human docs).
- Default subproject root: `.agents/projects/<slug>/`.
- Default agent-only root: `.agents/`.
- Default source-material root: `reference/`.
- Use `scripts/scaffold_project.py` for deterministic scaffolds.
- Never overwrite an existing `AGENTS.md`; report that `templates/AGENTS.md` must be merged manually.
- Keep `AGENTS.md` as the root entrypoint and put copied operating protocol in `.agents/AGENT-GUIDANCE.md`.
- Preserve existing `.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, `reference/README.md`, `.claude/settings.json`, and `.codex/config.toml`, and append to `.agents/log.md`, even when force-refreshing scaffold docs.
- Create `.claude/settings.json` (Claude Code `bypassPermissions`) and `.codex/config.toml` (Codex `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`) when absent so both runtimes run at maximum permissions without approval prompts.
- Fill known proposal context: product vision, principles, outcomes, assumptions, what good looks like, risks, non-goals, and next skills.
- Save unknowns as open questions instead of pretending alignment exists.

Recommended output:

- Scaffold path created or reused.
- Files created/skipped.
- Agent-only guidance path and any manual `AGENTS.md` merge note.
- Current phase.
- Missing proposal prerequisites.
- Next skill, usually `product-discovery`, `prototype`, `spec`, or `plan`.

## Status Orientation

Use this mode when the user asks what phase the project is in, what to do next, or where work left off.

Check:

- Root and nearest subproject `status.md`.
- `.agents/phases/`.
- `docs/product/`.
- `docs/decisions/`.
- `.agents/specs/`, `.agents/plans/`, `docs/tech-design/`, and `.agents/research/`.
- `.agents/prototypes/`, `.agents/qa/`, and `.agents/release/`.
- Open tasks, recent commits, issues, PRs, and local instructions.

Answer with:

- Current phase and confidence.
- Evidence.
- Missing required artifacts.
- Whether the trail answers what is being built, why it matters, and what good looks like.
- Skipped gates or Chesterton's-fence risks.
- Next gate.
- Next skills.
- One concrete next action.

For `next`, continue past the status answer only when that one concrete action is unambiguous and inside the user's requested scope. If two or more actions are plausible, ask one concise verification question.

If what/why/good is missing and the next action would harden product direction, recommend `product-discovery` or `spec` before build work.

## Repair And Introspection

Use this mode when status is stale, phase is ambiguous, core context is missing, or the user asks to get a project back on track.

- Compare actual artifacts to `references/project-phases.md`.
- Separate missing prerequisites from optional polish.
- Identify decisions or principles that explain the current shape before recommending changes.
- Update `.agents/status.md` when project-doc edits are in scope.
- If status cannot be updated, state why.

Repair output:

- Conformity verdict: on track, thin but usable, off track, or blocked.
- Evidence checked.
- Missing or weak artifacts.
- Recovery plan.
- First concrete action.

## Retro And Learning

Use this mode after a release, paused project, or meaningful work period.

- Separate shipped facts from guesses.
- Grade the result against proposal outcomes, principles, and what good looks like.
- Capture user, product, engineering, and business lessons.
- Recommend durable documentation updates.
- Do not edit global agent memory unless the user explicitly asks for a memory update.
