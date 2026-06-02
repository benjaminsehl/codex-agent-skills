# QA And Release Workflow

## Contents

- Live QA
- Health check
- Ship
- PR readiness
- PR Review Feedback
- GitHub Handoff
- Post-release learning

Use this reference from `qa` and `ship`. `ship` owns every GitHub conversation step from PR open onward (opening, review-thread replies, ready promotion).

## Live QA

- Identify the app, URL, build, feature, or user flow under test.
- Define user paths, personas, risks, and evidence to collect.
- Test like a user, not just like a developer.
- Record bugs with repro steps, expected behavior, actual behavior, severity, and evidence.
- When fixing, retest the exact repro and recommend regression coverage.

## Health Check

Use only for broad periodic readiness, not ordinary changed-code review.

Check:

- Tests and CI health.
- Performance and accessibility readiness.
- Security and dependency risk.
- Documentation and decision trail.
- Maintainability and architectural drift.

Output blockers, important fixes, quick wins, and one next action.

## Ship

- Decide binary `GO` or `NO-GO` — no tiers, no "soft go."
- Gather diff, tests, builds, CI, deployment path, feature flags, migrations, docs, and rollback path.
- Fan out specialist auditors in parallel by default: correctness, security, performance, data, migration, docs.
- Apply the migration gate, tiered by traffic state:
  - Pre-live (no production traffic, no real users): reckless migrations acceptable. Name the risk and proceed.
  - Live traffic (real users, real data): blocker by default. Require forward + reverse SQL, staging dry-run, locking analysis under concurrent writes, backfill plan, and a named owner who watches the rollout. Missing any → NO-GO.
- Separate blockers from accepted risks and nice-to-have fixes.
- Name rollback triggers and rollback procedure for live-traffic releases.
- For GitHub-backed work, confirm PR state, CI/check status, and reviewer-sub-agent findings. If no PR exists, open one and decide draft vs ready as an engineering call — do not ask the founder.
- Use product-impact framing for the PR description: what user capability ships, not what files changed.
- Carry the decision to completion by traffic state: when `pre-live`, merge and deploy autonomously; when `live`, ask the founder GO/NO-GO before merging to the default branch, then let deploy follow the approved merge.
- Do not run retro. Ship is pre-release only.

## PR Readiness

Use this on the way to merge. Draft-vs-ready and the ready promotion are engineering calls the agent makes — they do not require founder approval.

- Confirm the branch is pushed and the PR exists.
- Confirm targeted and broad verification has passed or clearly document accepted gaps.
- Run `review` against the final diff or PR, fanning out reviewer sub-agents.
- Run `code-simplify` on the changed files when simplification risk is reasonable.
- Fix important findings and rerun relevant checks.
- Update the PR body with final summary, verification, risk, and follow-up.
- Confirm the PR body explains why the work matters, the principles behind the change, and how the agent approached it.
- Promote the PR to ready autonomously once reviewer sub-agents are satisfied, simplification has run, and verification is green.
- Keep the PR draft if unresolved blockers, failing checks, or missing verification remain — or if an open product/UX decision is waiting on the founder.

## PR Review Feedback

Use this to address GitHub PR comments, requested changes, or unresolved review threads, whether from reviewer sub-agents or human reviewers.

- Resolve the PR from local branch context or the provided PR URL/number.
- Fetch thread-aware review state using GitHub MCP tools (or `gh api graphql` in CLI environments) — preserve review-thread IDs, resolution state, outdated state, file paths, and line anchors.
- Cluster actionable comments by behavior or file; separate fixes from questions, duplicates, stale threads, and non-actionable notes.
- Implement fixes traceably, keeping each change tied to the feedback it addresses.
- If a comment needs explanation rather than code, reply with the reasoning instead of forcing a code change.
- Commit and push fixes to the PR branch.
- Reply to and resolve review threads autonomously as part of the engineering loop — this is collaboration on the change, not external messaging.
- Escalate to the founder only when a comment raises a product/UX decision; surface it in product-implication language and leave the thread open until answered.
- Leave ambiguous or conflicting engineering feedback unresolved and explain the tradeoff.

## GitHub Handoff

Use this for opening, updating, promoting, and merging PRs. `build` pushes the branch; `ship` handles every GitHub conversation step from PR open onward, autonomously, gated only by traffic state and the always-ask floor.

- Check whether a PR already exists for the topic branch before opening one.
- Use the GitHub MCP `create_pull_request` (or `gh pr edit` in CLI environments) to open a PR when none exists, or to update an existing PR for the branch. Decide draft vs ready as an engineering call.
- Write a descriptive PR body using product-impact framing: what user capability ships, not what files changed. Cover: why this PR exists, the principles behind the change, how the agent approached it, what changed, verification, risks, and follow-up.
- Promote to ready autonomously once verification passes, reviewer sub-agents are satisfied, and no open product/UX decision remains.
- Read the `Traffic state:` field in `.agents/status.md` before merging. When `pre-live`, merge and deploy autonomously and name the risk. When `live`, ask the founder GO/NO-GO before merging to the default branch; deploy then follows the approved merge.
- If GitHub handoff is blocked by missing auth, no writable remote, branch protection, network failure, or unavailable tooling, do not loop. Report the blocker, the completed local work, verification status, and the exact next command, credential, or access step needed.
- Always-ask floor (any traffic state): the full floor in `references/agent-operating-protocol.md` is authoritative and applies in the handoff path too — including privacy-sensitive data, dropping tables or deleting production data, money movement, credential use, external messaging, and merging to the default branch when traffic state is `live`. In the GitHub path specifically, never force-push the default branch or delete branches with unmerged work without explicit founder direction.

## Post-Release Learning

- Grade against proposal outcomes, principles, and what good looks like.
- Capture what shipped, what users learned, what broke, and what changed.
- Record follow-up work in project docs.
- Propose memory updates only when the user explicitly asks for memory changes.
