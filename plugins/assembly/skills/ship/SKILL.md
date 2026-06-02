---
name: ship
description: Use when deciding whether a change is ready to release; produces a binary GO or NO-GO decision with blockers, risks, evidence, and rollback criteria.
---

# Ship

## Purpose

Decide whether a change is ready to release. The decision is binary: `GO` or `NO-GO`. A `GO` requires verification evidence and a rollback plan. Ship owns GitHub conversation: it opens the PR for branches `build` has pushed, decides draft vs ready, runs reviewer sub-agents, merges, and deploys.

How far a `GO` carries itself depends on traffic state (read `Traffic state:` in `.agents/status.md`; absent or unknown means `pre-live`):

- `pre-live`: a `GO` proceeds autonomously through merge and deploy. No founder check-in unless a product/UX decision is open or an always-ask floor item is involved.
- `live`: a `GO` carries autonomously up to a reviewed, ready PR, then asks the founder before merging to the default branch. The merge gate is a single product-impact question, not an engineering one; deploy follows the approved merge.

## References

- `references/workflows/qa-and-release.md`: ship mode, health-check mode, rollout, rollback.
- `references/security-checklist.md`: release security checks.
- `references/performance-checklist.md`: release performance checks.
- `references/testing-patterns.md`: verification evidence.

## Workflow

1. State that the `ship` workflow is active and identify the release candidate. If multiple slices are shippable, present 2-3 candidates with evidence and ask the founder to pick. Use the explicit options-list pattern.
2. Gather the diff, test/build/CI status, deployment path, feature flags, migrations, docs, and rollback mechanism.
3. Fan out specialist auditors in parallel by default: correctness, security, performance, data, migration, docs. Merge reports.
4. Apply the migration gate, tiered by traffic state:
   - Pre-live (no production traffic, no real users): reckless migrations are acceptable — drop tables, rename columns, no reverse SQL needed. Name the risk and proceed.
   - Live traffic (real users, real data): blocker by default. Require forward + reverse SQL, staging dry-run, locking analysis under concurrent writes, backfill plan, and a named owner who will watch the rollout. Missing any → NO-GO.
5. If no PR exists for the topic branch, open it now and decide draft vs ready as an engineering call — do not ask the founder. PR description uses product-impact framing: what user capability ships, not what files changed.
6. Promote draft to ready autonomously once reviewer sub-agents are satisfied, simplification has run, and verification is green. The ready transition is an engineering call, not a founder approval.
7. If GitHub handoff is blocked (gh CLI failure, no remote, missing access, network error), do not silently swallow it. Name the failed command, what work is completed locally, current verification status, and the next recovery step. The decision becomes NO-GO until handoff is unblocked.
8. Produce a single binary decision:
   - `GO`: verification green, blockers cleared, reviewer sub-agents satisfied, rollback trigger and procedure named, residual risks acknowledged, product-impact statement included.
   - `NO-GO`: blockers listed, recommended fixes named, next path to GO stated.
9. Carry a `GO` to completion by traffic state:
   - `pre-live`: merge and deploy autonomously. Report what shipped.
   - `live`: ask the founder GO/NO-GO before merging to the default branch, leading with the user-facing impact and the rollback plan; deploy follows the approved merge.
   - Escalate mid-flow only if a blocker turns out to be a product/UX decision (raise it in product-implication language) or an always-ask floor item appears.
10. Do not run retro. Ship is pre-release only.

## Verification

- Decision is binary: `GO` or `NO-GO` — no tiers, no "soft go."
- Test, build, CI, or manual verification status is named.
- Specialist fan-out is named; skipped specialists are justified.
- Migration gate is applied with explicit traffic-state classification.
- Blockers are separated from recommended fixes.
- Rollback trigger conditions and procedure are present for live-traffic releases.
- PR state is named; draft-vs-ready is decided autonomously, and merge matches traffic state.
- Traffic state is named, and the merge step matches it: autonomous when `pre-live`, founder GO/NO-GO when `live` (deploy follows the approved merge).
- PR description uses product-impact framing (what ships for users, not what code changed).
- Any accepted risk is explicit.

## Stop Conditions

- The rollback path is unknown for a live-traffic change.
- Critical security, data-loss, migration, or compliance risk is unresolved.
- Required verification is unavailable.
- A live-traffic migration is missing forward/reverse SQL, staging dry-run, locking analysis, backfill plan, or named owner.
- Traffic state is `live` and the next step is merging to the default branch — ask the founder GO/NO-GO.
- A blocker is actually a product/UX decision — raise it to the founder in product-implication language.
- Multiple shippable slices exist and choosing among them would be arbitrary.
