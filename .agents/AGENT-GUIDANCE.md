# Agent Operating Protocol

Use this protocol at the start of meaningful project work and whenever the user returns after time away.

## Contents

- Orient first
- Autonomy and escalation
- Phase prerequisites
- Skill routing
- Status escalation
- Prompt clarity
- Missing prerequisites
- Hard boundaries
- Output expectations

## Orient First

1. Read `.agents/status.md` if it exists.
2. If the work is inside a subproject, read the nearest `.agents/projects/**/status.md` that matches the requested area.
3. Check `.agents/log.md` and relevant `.agents/notes/` when resuming agent work or diagnosing skipped gates.
4. Check `.agents/phases/`, `docs/product/`, `docs/decisions/`, `.agents/specs/`, `.agents/plans/`, and relevant child `projects/`.
5. State the current phase and the skill you are using when that materially affects the work.

## Autonomy And Escalation

Assembly optimizes for the founder's attention. Two axes decide when to act autonomously and when to escalate. The default posture is high autonomy: act, validate with sub-agents, and leave evidence — escalate only when one of the two axes says to.

### Axis 1 — Decision type (applies in every traffic state)

- Product and UX decisions always go to the founder, framed in product-implication language — user scenarios, experience tradeoffs, and business or viability implications — never engineering-implementation detail. The agent flags the concern and does not decide it. An open product/UX decision pauses autonomous progress until the founder answers.
  - Product/UX decisions include: what gets built and why, user-facing behavior, copy, flow, or visual-design tradeoffs, scope cuts that change the user experience, naming, positioning, pricing, and business model.
- Engineering decisions are the agent's to make and run autonomously. Quality is assured by reviewer sub-agents — the `code-reviewer`, `security-auditor`, and `test-engineer` personas fanned out in parallel — not by founder approval. The founder is the product director, not the per-PR reviewer.
  - Engineering decisions include: architecture, libraries, file and module layout, test strategy, refactors, commit and branch hygiene, opening a PR and whether it is draft or ready, and merging engineering-only changes (subject to traffic state).
- When a step is mixed, split it: take the engineering decision autonomously and escalate only the product/UX part, in product-implication language.

### Axis 2 — Traffic state (founder-declared in `.agents/status.md`, default `pre-live`)

`.agents/status.md` carries a `Traffic state:` field. Only the founder sets it; the agent never silently flips it. Absent or unknown means `pre-live`.

- `pre-live` — no real users, no production traffic. When no product/UX decision is open and no always-ask floor item is involved, the agent runs the whole roadmap autonomously: write code, open PRs (its own call on draft vs ready), run reviewer sub-agents, merge to the default branch, and deploy — across as many PRs as the roadmap needs, without per-action check-ins.
- `live` — real users and real traffic. Everything up to merge stays autonomous (write code, open PRs, run reviewer sub-agents). Merging to the default branch becomes a founder GO/NO-GO: the agent prepares the release decision (verification, risk, rollback) and asks before merging; deploy then follows the approved merge.

### Always-ask floor (any traffic state)

These never run autonomously regardless of traffic state or product-gate clarity:

- Money movement, purchases, or trades.
- Credential or secret use or exposure.
- External messaging or communication on the founder's behalf.
- Privacy-sensitive data handling.
- Irreversible destructive operations: force-push to the default branch, deleting branches with unmerged work, dropping tables, deleting production data.
- Merging to the default branch when traffic state is `live`.
- Anything the target repo's local protocol explicitly marks ask-first.

### What is no longer an interruption

Do not stop to ask about these — they are engineering calls the agent owns:

- Opening a draft PR, choosing draft vs ready, or promoting a PR to ready.
- Merging engineering-only PRs when `pre-live`; opening, reviewing, and readying them (but not merging) when `live`.
- Deploying when `pre-live`, and deploying from a founder-approved merge when `live`.
- Per-action engineering approvals or phase-ceremony confirmations.

## Phase Prerequisites

Proposal needs:

- Product vision.
- Product principles.
- Desired outcomes.
- Assumptions.
- What good looks like.

Prototype needs:

- Prototype question.
- Artifact plan.
- Success criteria.
- Link back to the proposal.

Build needs:

- Approved spec.
- Implementation plan.
- Acceptance criteria.
- Verification path.

Release needs:

- QA scope.
- Ship criteria.
- Rollback or hold criteria.
- Grade against the original proposal.

## Skill Routing

- User says "next", "continue", or "do the next normal thing": use `next`.
- Unknown phase, returning session, scaffold, recovery, retro, or durable project learning: use `project-status`.
- Raw idea, product ambition, business viability, or planned UX critique: use `product-discovery`.
- Tangible learning before production build: use `prototype`.
- Requirements before coding: use `spec`.
- Task breakdown after spec: use `plan`.
- Implementation: use `build`.
- Verification: use `test` or `qa`.
- Pre-merge quality: use `review` or `code-simplify`.
- Release decision: use `ship`.

## Status Escalation

`project-status` is the first stop. It should answer the phase and next skill when the paper trail is clear, and switch into repair mode when it is not.

Use repair mode when:

- The current phase is ambiguous.
- Required artifacts for the apparent phase are missing or contradictory.
- The user asks "what should we do?" and the answer depends on repairing project context.
- The project has skipped gates that should be recorded before more work continues.
- `.agents/status.md` is stale, absent, or no longer matches the actual work.

## Prompt Clarity

If the user prompt is unclear, state the inferred task and verify before acting.

Use this shape:

```text
I think you want me to <inferred task>. I see the project is in <phase>. I would use <skill> next because <reason>. Is that right?
```

Ask only when the ambiguity changes the work, risk, or phase.

## Missing Prerequisites

If the prompt is clear but the current phase is missing important context:

1. Warn briefly.
2. Name the missing prerequisite.
3. Recommend the double-back skill.
4. Ask only if skipping would materially change scope or risk.

Use this shape:

```text
I can do that, but we are missing <artifact>. The safer next step is <skill> so we can <reason>. If you still want to proceed, I will continue and mark this as a skipped gate.
```

If the user insists, proceed unless the request crosses a hard safety boundary. In the final response, record the skipped gate and risk. When editing project docs is in scope, also update `.agents/status.md`.

## Hard Boundaries

Neither user insistence nor traffic-state autonomy overrides the always-ask floor above, or:

- Privacy and credential boundaries.
- Destructive filesystem or data operations.
- External messages, purchases, trades, money movement, or account changes.
- Security, legal, medical, or financial safety checks.
- Repository instructions that explicitly require confirmation.

## Output Expectations

For phase-sensitive work, the final response should include:

- Phase used.
- Traffic state assumed (`pre-live` or `live`) when the work reached merge, deploy, or release.
- Skill used or recommended.
- Evidence checked.
- Missing prerequisites, if any.
- Open product/UX decisions raised for the founder, if any, in product-implication language.
- Verification performed, including reviewer sub-agent fan-out when the change merged or shipped.
- Skipped gates, if the user insisted on skipping them.
