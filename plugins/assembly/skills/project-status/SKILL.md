---
name: project-status
description: Project orientation gateway. Use when returning to work, checking phase, repairing stale status, running a retro, or asking what to do next. For new project scaffolds, route to `init`.
---

# Project Status

## Purpose

Orient the project before work continues. Determine the active project or subproject, current phase, missing prerequisites, next gate, and next skill. Frame what shipped and what ships next in product-impact language.

This is the gateway for status, repair, retro, and routing. For scaffolding a new project or subproject workspace, route to `init`. Do not route to separate `new-project` or `introspect` skills; use the references below.

## References

- `references/project-phases.md`: phase gates and status output shape.
- `references/project-kernel-structure.md`: root `docs/` and recursive subproject structure.
- `references/agent-operating-protocol.md`: unclear prompts, missing prerequisites, skipped gates, and safety boundaries.
- `references/workflows/project-lifecycle.md`: scaffold, status, repair, retro, and learning modes.
- `references/hyper-project-notes.md`: only for retrofitting scattered Hyper-style notes.

## Workflow

1. State that `project-status` is active and identify the repo plus project or subproject.
2. Inspect `.agents/status.md`, nearest `.agents/projects/**/status.md`, phase files, product docs, decisions, specs, plans, tech design, research, prototypes, QA/release notes, `.agents/log.md`, relevant `.agents/notes/`, `reference/`, open tasks, and recent commits.
3. If project docs are missing and the founder is starting or restarting work, recommend `init` and stop here; do not run the scaffold script from this skill.
4. Classify the phase:
   - Proposal: outcomes, assumptions, principles, or success criteria are not aligned.
   - Prototype: direction needs tangible proof before production build.
   - Build: approved direction exists and implementation slices are active.
   - Release: built work needs QA, polish, ship decision, and follow-up capture.
5. Apply Chesterton's fence: name the decision, principle, or historical artifact that explains the current shape before recommending replacement.
6. If phase, status, or recovery path is unclear, run repair mode: audit conformance, update `.agents/status.md` when project-doc edits are in scope, and produce a recovery plan.
7. If multiple active slices exist, present 2-3 candidates with evidence and ask the founder to pick. Use the explicit options-list pattern — do not pick arbitrarily.
8. Output:
   - Current phase with evidence.
   - What shipped most recently, framed as user-facing capability (not "merged PR #42").
   - What ships next, framed as user-facing capability.
   - Missing artifacts vs optional polish.
   - Skipped-gate risks.
   - Next gate, next recommended skill, one concrete next action.
9. Include whether the project trail clearly answers what is being built, why it matters, and what good looks like. If not, recommend `product-discovery` or `spec` before build/release work.

## Verification

- The phase verdict cites actual files, diffs, commits, tasks, or notes.
- What-shipped and what-ships-next statements use product-impact language, not code-changed language.
- Missing artifacts are separated from optional polish.
- Skipped gates and their risks are named when the founder asks to move ahead anyway.
- Recommended skills match the current phase and blockers.
- `.agents/status.md` is updated when project-doc edits are in scope, or the reason for not updating it is stated.
- What/why/good gaps are named instead of hidden inside a confident next step.
- Multiple-slice ambiguity produces a 2-3-option pick list, not an arbitrary choice.
- The founder can resume with one clear next action.

## Stop Conditions

- There is no accessible repo, project folder, or artifact trail to assess.
- The current state depends on private external systems that are unavailable.
