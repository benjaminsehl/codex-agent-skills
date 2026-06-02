# Engineering Delivery Workflow

## Contents

- Spec
- Plan
- Build
- Test
- Review
- Code simplify
- Branch push

Use this reference from `spec`, `plan`, `build`, `test`, `review`, and `code-simplify`. PR opening, review feedback, and ready promotion live in `qa-and-release.md` — `ship` owns every GitHub conversation step from PR open onward.

## Spec

- Run mini-discovery before drafting (max 4 questions per round, focused on user, pain, wedge). Always fire, even when the spec is being repaired or invoked via routing from `build`.
- Tier the spec by signal density: lightweight when fresh discovery exists; full when signals are thin.
- Surface assumptions, non-goals, and open questions before treating the spec as final.
- Save the spec to `.agents/specs/` (Assembly-native) or the repo convention, for example `SPEC.md`.
- Stop at founder review. Do not auto-continue into planning.

## Plan

- Start from an approved spec or equivalent requirements.
- Write each task with a thin contract: acceptance criteria, verification, files touched, dependencies.
- Add checkpoints after meaningful phases.
- If the plan crosses 5 tasks, flag for founder sign-off before saving.
- Re-enter `plan` mid-stream when `build` surfaces evidence that contradicts the plan: name the contradicting evidence, revise affected tasks, update plan docs, continue.
- Stop at founder review before implementation.

## Build

Build is a router, not a dispatcher. It implements code for an approved task and routes to other skills at phase boundaries.

- Treat an empty or minimal `build` prompt as permission to identify the next implementable task from project evidence, not to execute every phase.
- Route — do not execute — when a phase is missing: spec missing → invoke `spec` (mini-discovery still fires); plan missing → invoke `plan`; multiple plausible tasks → present 2-3 candidates with evidence and ask the founder.
- Before modifying tested legacy code, write or identify characterization tests covering current behavior. Required, not "where practical."
- For new behavior, write the failing/targeted test before implementation.
- Make the smallest complete change. Keep unrelated cleanup out of scope.
- Run targeted verification and the broadest practical regression check.
- Re-enter `plan` mid-task when contradicting evidence is structural (wrong assumption, hidden dependency, simpler path discovered) rather than a local bug. Do not silently work around stale tasks.
- After implementation, route — do not auto-run — for downstream phases: recommend `test` if behavior is unverified, `review` if verified-unreviewed, `code-simplify` after review when safe.
- For material changes in a GitHub-backed repo, commit on a topic branch and push. Do not open PRs — that is `ship`'s job.

## Test

- Classify coverage tier by criticality: critical path (money movement, auth, data integrity, irreversible operations) → full coverage including characterization for adjacent legacy paths; standard feature → targeted unit + happy path + worst plausible failure; internal/utility → targeted unit only.
- Before modifying tested legacy code inside critical-path or standard-feature surfaces, write characterization tests that lock current behavior.
- For bugs, prove the bug with a failing test before fixing (Prove-It).
- For new behavior, write tests that describe the intended outcome.
- Use browser/runtime verification for UI behavior.
- Report targeted and broader check results separately.

## Review

- Inspect the diff plus relevant surrounding code.
- For PRs, use GitHub MCP tools for PR metadata, changed files, checks, and review-thread context.
- Fan out specialist reviewers in parallel by default: correctness, architecture, security, performance, tests. Skip a specialist when the diff demonstrably does not touch its surface; name what was skipped and why.
- Lead with findings ordered by severity. Include file and line references for concrete issues.
- `review` itself surfaces findings; the agent then resolves engineering findings autonomously (via `build` or `code-simplify`) as part of the delivery loop. Escalate a finding to the founder only when it is a product/UX tradeoff, in product-implication language.
- If there are no findings, say so and name residual risk.

## Code Simplify

- Preserve behavior exactly.
- Prefer clearer names, guard clauses, smaller functions, removed duplication, and deleted dead code.
- Characterize behavior before changing risky code.
- Verify after each meaningful step.
- Abandon simplifications that cannot be proved safe.

## Branch Push

Use this for material changes in a git repo with a GitHub remote, run from `build` before handing off to `ship`.

- Inspect branch, remote, and status before committing.
- Keep commits focused; do not include unrelated user changes.
- Prefer a topic branch over committing directly to `main`.
- Use a switch pattern that works for both existing and new branches.
- Stage intentionally, commit with a clear message, and push.
- If push is blocked (missing auth, no writable remote, network failure), do not loop. Report the failed command, completed local work, verification status, and the exact next recovery step.

Suggested command flow:

```bash
git status --short --branch
git branch --list <topic-branch>
git switch <topic-branch> || git switch -c <topic-branch>
git add <intentional-files>
git commit -m "<focused message>"
git push -u origin HEAD
```

Build stops after the branch is pushed. PR creation, review feedback, and ready promotion live in `ship` — see `qa-and-release.md`.
