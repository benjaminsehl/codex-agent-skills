# Agent Instructions

This project follows a phase-aware product-building workflow.

## Start Here

Before meaningful work, read:

- `docs/status.md`
- The nearest matching `docs/projects/**/status.md`, if working in a subproject
- `.agents/AGENT-GUIDANCE.md`
- Relevant files under `docs/phases/`, `docs/product/`, `docs/decisions/`, `docs/specs/`, and `docs/plans/`

If these files do not exist yet, use `init` to scaffold them.

## Phase Awareness

Always identify the current project phase before choosing a workflow:

- Proposal: align on outcomes, assumptions, principles, and what good looks like.
- Prototype: create tangible proof before production build.
- Build: implement approved specs in verified slices.
- Release: QA, polish, ship or hold, grade against proposal, and capture follow-up learning.

Use `init` when scaffolding a new project or subproject workspace.
Use `project-status` when returning to a project, repairing stale status, running a retro, or when the phase is unclear.
Use `next` when the user asks to continue through the normal process and the next action should be selected from project context.

## Skill Routing

- These route names refer to the Assembly plugin's phase-aware lifecycle workflows.
- If another installed skill has the same name, prefer Assembly for project lifecycle decisions in this repo.
- Contextual continuation: `next`
- New project or subproject scaffold: `init`
- Status, repair, retro, or project learning: `project-status`
- Raw idea, scope, ambition, business viability, or UX before build: `product-discovery`
- Tangible proof: `prototype`
- Requirements: `spec`
- Task breakdown: `plan`
- Implementation: `build`
- Tests and runtime verification: `test` or `qa`
- Quality pass: `review` or `code-simplify`
- Release decision: `ship`

## Capabilities

Domain skills assembled for this project's stack via the capability-acquisition
behavior (`init` seeds them, `build` adds them just-in-time, `project-status`
re-runs it). Each entry: skill name, source, why. Mirror of the status block's
`capabilities:` list where that block exists. See the plugin's
`references/capability-acquisition.md`.

- _none yet_

## Autonomy And Escalation

Reserve founder attention for product and UX decisions; run engineering autonomously.

- Product/UX decisions — what gets built and why, user-facing behavior, copy, flow, scope cuts that change the experience, naming, pricing — always escalate to the founder in product-implication language (user scenarios, not engineering detail).
- Engineering decisions are the agent's call, validated by reviewer sub-agents (`code-reviewer`, `security-auditor`, `test-engineer`), not by founder approval. Opening a PR, choosing draft vs ready, and merging engineering-only changes are not interruptions.
- Traffic state lives in `docs/status.md` (`Traffic state:`, founder-set, default `pre-live`). When `pre-live`, run the whole roadmap — PRs, merges, deploys — autonomously. When `live`, keep opening and reviewing PRs autonomous and ask the founder GO/NO-GO before merging to the default branch; deploy follows the approved merge.
- Always-ask floor (any traffic state): money, credentials, external messaging, privacy-sensitive data, irreversible destructive operations, and merging to the default branch when live.

Full detail is in `.agents/AGENT-GUIDANCE.md`.

## Unclear Prompts

If the prompt is unclear, state what you think the user wants, name the current phase, recommend the next skill, and verify before acting.

## Missing Phase Context

If the user asks to skip ahead while important phase context is missing, warn them, name the missing artifact, and recommend the double-back skill first.

If the user insists, proceed unless the request crosses a hard safety, privacy, destructive, credential, money movement, external messaging, or confirmation boundary. Record skipped gates in the final response and update `docs/status.md` when project-doc edits are in scope.

## Paper Trail

Preserve Chesterton's fence. Before changing or removing an existing structure, look for the decision, principle, plan, or status note that explains why it exists.
