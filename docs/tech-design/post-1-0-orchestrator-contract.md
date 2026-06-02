# Tech Design: Post-1.0 Orchestrator And Assembly Contract

Last updated: 2026-05-27
Status: draft direction, post-1.0

## Purpose

Define the contract a post-1.0 orchestrator would use to coordinate Assembly-driven agent work.

This is not a 1.0 implementation requirement. It exists so 1.0 decisions do not accidentally block the later orchestrator.

## Design Principles

- Assembly remains the project-local protocol.
- The orchestrator reads and writes through visible project artifacts.
- Founder approval gates stay explicit.
- Agent sessions should receive bounded tasks with clear ownership.
- Every session returns evidence, not just prose.
- Automation should preserve Chesterton's fence by linking changes to prior decisions.

## Project State Inputs

The orchestrator should read:

- `AGENTS.md`
- `.agents/AGENT-GUIDANCE.md`
- `.agents/log.md`
- `.agents/notes/`
- `.agents/status.md`
- `.agents/phases/`
- `docs/product/`
- `docs/decisions/`
- `.agents/specs/`
- `.agents/plans/`
- `.agents/prototypes/`
- `.agents/qa/`
- `.agents/release/`
- `.agents/projects/`
- `reference/`
- Git branch, commits, PRs, comments, checks, and reviews

## Minimum Status Shape

Markdown remains the source of truth for 1.0. The orchestrator may later benefit from a small machine-readable block:

```yaml
project: assembly
phase: proposal
current_gate: spec
next_skill: plan
blocked: false
needs_founder_input: false
last_verified: 2026-05-27
```

Do not add this until a real orchestrator spike proves it is useful.

## Work Assignment Packet

The orchestrator should create bounded agent assignments with:

- Repo and project/subproject.
- Phase and gate.
- Skill to use.
- Specific task.
- Files or docs to inspect first.
- Ownership boundaries.
- Verification requirements.
- Ask-first boundaries.
- Expected handoff artifact.

## Evidence Packet

Each agent session should return:

- What changed.
- Why it changed.
- Files touched.
- Commands run.
- Verification results.
- PR URL or local-only reason.
- Open risks.
- Skipped gates.
- Next recommended skill.
- Status/docs updated.

## Approval Boundaries

The orchestrator must pause for:

- Founder/product judgment.
- Marking draft PRs ready.
- Merge.
- Deploy.
- Destructive operations.
- Credential or privacy-sensitive work.
- Money movement, purchases, trades, or account changes.
- External messaging.

## Failure Modes To Design Against

- The orchestrator dispatches work without enough product context.
- Multiple agent sessions edit overlapping files.
- A sidecar reviewer becomes the patch owner by accident.
- A stale status file sends work down the wrong path.
- The system rewards activity over evidence.
- The founder gets asked too late, after product direction has already hardened.

## Open Questions

- Should the orchestrator update markdown directly or always ask an agent session to update project docs?
- What is the smallest structured status layer that helps without duplicating docs?
- How should the orchestrator model subprojects and nested roadmaps?
- Which quality signals should block new work from starting?
