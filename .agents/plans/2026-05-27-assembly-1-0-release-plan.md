# Plan: Assembly 1.0 Release

Last updated: 2026-05-27
Status: draft

## Goal

Release Assembly 1.0 as a reliable dual-runtime project operating system (Codex and Claude Code) for a human-led agentic app factory.

## Release Principle

1.0 should feel small, solid, and useful. It should not pretend to be the post-1.0 orchestrator yet.

## Milestones

### 1. Spec Gate

Outcome: the 1.0 behavior spec and north-star vision are coherent enough for implementation and proof.

Tasks:

- Align `.agents/specs/assembly-1-0.md` with the human-led app factory vision.
- Add app-factory north-star and research synthesis docs.
- Define what is blocking for 1.0 versus deferred to the post-1.0 orchestrator.
- Update `.agents/status.md` with the current gate and next skills.

Exit evidence:

- Spec names release blockers.
- Roadmap separates 1.0 from post-1.0.
- Status points to the right next action.

### 2. Dual-Runtime Control Loop Release Candidate

Outcome: the plugin behavior matches the 1.0 spec in both Codex and Claude Code.

Tasks:

- Verify `next` uses project status, phase gates, and clarification behavior in both runtimes.
- Verify `product-discovery` interviews by default in both runtimes.
- Verify minimal `build` prompts infer the next build-track gate in both runtimes.
- Verify GitHub handoff creates or updates descriptive draft PRs in both runtimes.
- Verify ready-for-review, merge, deploy, and privacy-sensitive actions remain ask-first boundaries in both runtimes. `ship` always asks before opening PRs or promoting to ready, regardless of product-gate clarity. The always-ask floor (money, credentials, external messaging, irreversible destructive ops) is honored on top.

Exit evidence:

- Validator output.
- Smoke prompt notes for Codex and Claude Code.
- One PR handoff using Assembly's own flow.

### 3. Assembly Self-Host Proof

Outcome: Assembly's own repo demonstrates the workflow from proposal through release.

Tasks:

- Use this branch as the spec/proposal proof.
- Turn accepted spec into implementation tasks.
- Run validators and smoke checks.
- Open or update a descriptive draft PR.
- Run self-review and code simplification where useful.
- Capture QA and release evidence.
- Capture a short retro after merge.

Exit evidence:

- PR includes why, principles, approach, verification, risks, and follow-up.
- `.agents/qa/assembly-1-0-smoke-evidence.md` records actual checks.
- `.agents/release/assembly-1-0-checklist.md` reaches a clear go/no-go.

### 4. CFO External Proof

Outcome: a real restart/greenfield project can use the scaffold and continuation loop.

Tasks:

- Run project-status/scaffold against `/Users/sai/cfo` only with explicit local scope.
- Confirm scaffold preserves any existing instructions.
- Update CFO status with phase and next gate.
- Run a minimal `next` or `project-status` continuation check.
- Record proof in `.agents/projects/cfo-proof/status.md`.

Exit evidence:

- CFO proof status records what was tested and what was intentionally not changed.
- Any private finance data remains unstaged and unprinted.

### 5. Release

Outcome: Assembly 1.0 is public, installable, and locally upgraded in both Codex and Claude Code.

Tasks:

- Confirm install and upgrade commands in Codex.
- Confirm install and upgrade commands in Claude Code.
- Confirm active skill list exposes only the candidate public skill surface (currently 13 skills) in both runtimes; any drift from that set is intentional and recorded.
- Confirm composer icon and metadata render in both runtimes.
- Merge the release PR after explicit approval.
- Upgrade the local plugin in both runtimes.
- Record release retro.

Exit evidence:

- Tag or version bump.
- Local plugin cache shows the released version.
- Release checklist is complete or explicitly held.

## Deferred Until After 1.0

- Post-1.0 orchestrator implementation.
- Dream/desloppification automation.
- Hosted dashboard.
- Runtimes beyond Codex and Claude Code.
- Automatic deploy/merge/branch cleanup.
- Background roadmap execution.

## Current Next Step

Finish the spec gate, then use `plan` to break the release candidate work into concrete implementation tasks.
