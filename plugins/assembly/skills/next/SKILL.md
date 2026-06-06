---
name: next
description: Contextual next-action dispatcher. Use when the user says "next", "continue", "do the next thing", or asks to proceed through the normal project process.
---

# Next

## Purpose

Choose and perform the next normal workflow step without guessing. Use project docs, phase gates, and recent evidence to decide the next specific skill or action. Frame progress in product-impact language.

`next` is intentionally narrow: it is a dispatcher for continuation, not a replacement for `project-status` or the lifecycle skills.

## References

- `references/project-phases.md`: phase gates, required evidence, and recommended skills.
- `references/agent-operating-protocol.md`: unclear prompts, skipped prerequisites, and safety boundaries.
- `references/workflows/project-lifecycle.md`: status orientation, repair, retro, and learning modes.
- `references/workflows/qa-and-release.md`: PR readiness under the product-gates-first model.

## Workflow

1. State that `next` is active and identify the repo plus project or subproject.
2. Read `AGENTS.md`, root `.agents/status.md`, nearest subproject `status.md`, `.agents/log.md` when present, and any task/spec/plan file explicitly named by status.
3. Determine the active phase, last completed gate, missing required evidence, and whether the next step is safe to infer.
4. If there is no Assembly project trail in this repo, do not stop and do not auto-scaffold. Ask the founder once whether to scaffold the project (one-question handoff). On confirmation, hand off to `init` for scaffolding and continue from the new trail.
5. If status is stale, contradictory, or missing, perform the `project-status` repair behavior first: audit the project trail, update `.agents/status.md` when project-doc edits are in scope, and report the recovery path.
6. Before dispatching into prototype, spec, plan, build, or release work, check whether the project trail answers the product gates:
   - What is being built (user capability, not code).
   - Why it matters (user pain it removes).
   - What good looks like (success criteria).
   - Risks and non-goals.
   - Rollback or hold criteria (when the change touches production behavior).

   If any product gate is missing and the founder has not delegated judgment, ask concise questions in product-implication language (never engineering-implementation detail). Flag business, user, and viability concerns; do not decide them. Route to `product-discovery` or `spec` when the gap is too large for inline questions.
7. If exactly one next step is unambiguous and low-risk, load and follow that public skill's workflow before running the step:
   - Proposal gaps: use `product-discovery` or `spec`.
   - Prototype gaps: use `prototype`.
   - Build gaps: use `spec`, `plan`, `build`, `test`, `review`, or `code-simplify` as the next unfinished gate requires.
   - Release gaps: use `qa`, `review`, or `ship`.
   - GitHub handoff gaps: `build` commits and pushes the branch; `ship` opens the PR, decides draft vs ready, runs reviewer sub-agents, and (when `pre-live`) merges and deploys — autonomously. Honor the always-ask floor regardless of traffic state, and ask the founder before merging to the default branch when traffic state is `live`.
8. If multiple plausible next steps exist, do not pick arbitrarily and do not ask a single narrow question. Use the explicit options-list pattern: 2-3 highest-leverage candidates, each with its evidence, asking the founder to pick.
9. If the founder asks to skip a missing prerequisite, warn once, name the skipped gate and the product risk it would have caught, then proceed only when the founder insists and no always-ask floor item applies.
10. End by naming the action taken (framed as user-facing capability where applicable), evidence used, status/docs updated or intentionally left unchanged, and the next expected gate.

## Gating Model

- Two axes decide escalation. Axis 1 — decision type: product/UX decisions always go to the founder in product-implication language; engineering decisions run autonomously, validated by reviewer sub-agents. Axis 2 — traffic state (`.agents/status.md` `Traffic state:` field, founder-set, default `pre-live`).
- Product gates — what is being built, why it matters, what good looks like, risks, and rollback — open the engineering rails. Once those gates are clear and verification is green, the engineering sequence continues through `build` → `ship` without per-action approval. `ship` opens PRs, decides draft vs ready, runs reviewer sub-agents, merges, and deploys — asking the founder only at the merge gate when traffic state is `live` (deploy then follows the approved merge).
- Always-ask floor (any traffic state): money movement, credentials, privacy-sensitive data, external messaging, irreversible destructive operations (force-push to default branch, delete branches with unmerged work, drop tables, delete production data), merging to the default branch when traffic state is `live`, and merge/deploy when verification is not green or reviewer sub-agents flag unresolved material concerns.

## Verification

- The chosen next action cites project files, status, commits, tasks, tests, or plans.
- The response explains why this action is next instead of merely saying it was inferred.
- Ambiguous forks produce a 2-3-option pick list with evidence, not a single narrow question.
- Stale or missing status triggers repair behavior before continuation.
- Product-gate gaps trigger concise questions in product-implication language or the appropriate double-back skill.
- PR opening and ready-promotion are routed to `ship`, not done inside `next` or `build`.
- Skipped gates are recorded in the response and in `.agents/status.md` when project-doc edits are in scope.

## Stop Conditions

- The next action would touch an always-ask floor item without explicit founder approval.
- Choosing among multiple active project slices would be arbitrary — use the pick list instead.
