---
name: build
description: Use when implementing the next planned task. Router model — implements code, routes to other skills at phase boundaries.
---

# Build

## Purpose

Implement the next planned task. Build is a router, not a dispatcher: it executes code changes for an approved task and routes to other skills when phases are missing or recommended.

## References

- `references/workflows/engineering-delivery.md`: build mode, incremental implementation, test-first behavior, debugging, and git hygiene.
- `references/testing-patterns.md`: testing patterns and regression coverage.
- `references/project-phases.md`: build prerequisites and engineering phase gates.
- `references/agent-operating-protocol.md`: unclear prompts, skipped prerequisites, and hard boundaries.

## Workflow

1. State that the `build` workflow is active. If no target task was provided, say you are inferring the next implementable task from the project trail.
2. Orient from `AGENTS.md`, `.agents/status.md`, relevant `.agents/specs/`, `.agents/plans/`, task files, current branch, and git status. Use the nearest project or subproject trail.
3. Check phase prerequisites in order. Route — do not execute — when a phase is missing:
   - Spec missing or stale → stop and invoke `spec` (which always runs mini-discovery first, even when invoked from build).
   - Plan missing or stale → stop and invoke `plan`.
   - Multiple plausible tasks exist → present 2-3 candidate tasks with evidence and ask the founder to pick. Use the explicit options-list pattern.
   - One unambiguous pending task → implement it.
4. Load acceptance criteria, relevant source files, and project commands for the chosen task.
5. If the task modifies tested legacy code, write or identify characterization tests covering current behavior before changing anything. Required, not "where practical."
6. For new behavior changes, write or identify the failing/targeted test before implementation.
7. Make the smallest complete change that satisfies the acceptance criteria.
8. If tests, build, or runtime checks fail, isolate the root cause before changing approach.
9. If implementation surfaces evidence that contradicts the plan structurally (wrong assumption, hidden dependency, simpler path discovered) — not just a local bug — stop and re-enter `plan` rather than working around stale tasks.
10. Run targeted verification and the broadest practical regression check.
11. After implementation, route — do not auto-run — for downstream phases:
    - Behavior unverified → recommend `test`.
    - Verified but unreviewed → recommend `review`, then `code-simplify` when safe.
    - Material change ready for backup → commit on the topic branch and push (no PR). `ship` opens the PR, runs reviewer sub-agents, merges, and deploys autonomously per traffic state — `build` does not wait for founder approval to hand off. If push itself fails (no remote, network error, missing access), name the failed command and the local state — do not silently move on.
12. Update task/status docs after verification passes or skipped checks are explained.

## What Build Does Not Do

- Does not open PRs — `ship` handles GitHub conversation.
- Does not auto-write specs or plans — routes to those skills.
- Does not promote drafts to ready — `ship` decides.

## Verification

- Chosen task and its phase prerequisites are named with evidence.
- Characterization tests exist before touching tested legacy code.
- Changed files are named.
- Tests or checks run are reported with results.
- The task acceptance criteria are satisfied.
- Topic branch is pushed when the change is material; PR creation is deferred to `ship`.
- Any skipped verification has a concrete reason.

## Stop Conditions

- Spec or plan is missing — route, do not invent.
- Multiple plausible tasks exist and choosing among them would be arbitrary.
- Missing product decisions would materially change what should be built and the founder has not delegated those decisions.
- The chosen task is too broad to complete safely in one slice and cannot be split from existing docs.
- Verification fails and cannot be isolated without changing scope.
- The task crosses an ask-first boundary.
