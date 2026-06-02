# Smoke Tests

These smoke tests verify that the public skills route correctly and do not rely on deleted support skills.

## Prerequisites

### Claude Code

```text
/plugin marketplace add benjaminsehl/assembly
/plugin install assembly@assembly
```

If the marketplace was already registered:

```text
/plugin marketplace update assembly
```

After enabling, confirm `Assembly` appears in `/plugin list` and a cache bundle exists under `~/.claude/plugins/cache/assembly/assembly/`.

### Codex

```bash
codex plugin marketplace add benjaminsehl/assembly
```

If the plugin was already registered:

```bash
codex plugin marketplace upgrade assembly
```

After enabling and restarting Codex, confirm `Assembly` appears in the active plugin list and that a cache bundle exists under `~/.codex/plugins/cache/assembly/assembly/`.

## Test Matrix

| Public skill | Smoke prompt | Expected evidence |
| --- | --- | --- |
| `next` | "Use next to do the next normal thing." | Reads project status, names phase/evidence, runs the next unambiguous skill or asks one concise question. |
| `project-status` | "Use project-status to tell me what phase this project is in." | Phase verdict with evidence, missing artifacts, next gate, next skills, and one action. |
| `project-status` | "Use project-status to scaffold a project called Habit Coach." | Creates `docs/`, `.agents/AGENT-GUIDANCE.md`, `.agents/log.md`, `.agents/notes/`, `reference/`, and reports skipped files or manual `AGENTS.md` merge. |
| `project-status` | "Use project-status to get this stale project back on track." | Conformity verdict, status update or skip reason, recovery plan, and next action. |
| `product-discovery` | "Use product-discovery on an app that summarizes my meetings." | Interview-first response with high-leverage questions before making product calls, unless the prompt delegates decisions. |
| `product-discovery` | "Use product-discovery and make the calls for an app that summarizes my meetings." | Delegated discovery brief with labeled assumptions, pain, wedge, alternatives, founder/business/design risks, and evidence needed. |
| `prototype` | "Use prototype to explore three onboarding directions before build." | Prototype question, throwaway artifact, inspection path, and verdict. |
| `spec` | "Use spec to define a tiny CLI that reverses lines from stdin." | Spec with assumptions, commands, boundaries, and success criteria. |
| `plan` | "Use plan on the approved spec and create implementation tasks." | Task list with dependencies, acceptance criteria, and verification steps. |
| `build` | "Use build to implement the first task." | One slice implemented with changed files and verification. |
| `build` | "Use build." | Reads project trail, infers the first unambiguous engineering gate, then specs, plans, implements, tests, reviews, simplifies, or opens draft PR as appropriate. |
| `build` | "Use build, then push this up." | Focused commit, pushed topic branch, descriptive draft PR created with `gh`, and why/principles/approach/verification in the PR body. |
| `build` | "Use build to address the unresolved PR review comments on PR #1." | Thread-aware comment read, traceable fixes, pushed update, replies and resolution only when explicitly requested. |
| `test` | "Use test to prove blank input returns blank output." | Failing or targeted test evidence, then passing result. |
| `qa` | "Use qa on this local app." | Tested flows, repro steps for bugs, evidence, and regression recommendations. |
| `review` | "Use review on the current diff." | Findings first, file/line references when issues exist, and test gaps. |
| `code-simplify` | "Use code-simplify on the changed files." | Behavior-preserving cleanup with verification evidence. |
| `ship` | "Use ship to decide whether this is ready to release." | GO/NO-GO, blockers, risks, evidence, rollback, PR readiness, and follow-up learning. |

## Claude Code Agents and Hooks

These surfaces are Claude Code only; Codex ignores them.

| Surface | Smoke check | Expected evidence |
| --- | --- | --- |
| Agents | After enabling, run `/agents` (or check `@agent-assembly:code-reviewer`). | `code-reviewer`, `security-auditor`, and `test-engineer` are listed for the Assembly plugin. |
| Agents | "Use review on the current diff." | `review` fans out to the specialist subagents and merges findings. |
| SessionStart hook | Start a session in a repo that has `.agents/status.md`. | Session opens with an Assembly primer naming the current phase and recommended next skills. |
| SessionStart hook | Start a session in a directory with no `.agents/status.md`. | No Assembly primer is injected. |
| Ask-first guard | Ask the agent to run `git push --force`, `gh pr merge`, or `wrangler deploy`. | A confirmation prompt appears citing the ask-first floor, even under `bypassPermissions`. |
| Ask-first guard | Ask the agent to run a normal `git push` of a topic branch, or `npm install`. | No extra prompt; the command proceeds through the normal flow. |

The hook scripts can also be exercised directly without a session:

```bash
# Guard: prints an "ask" decision for a boundary command, nothing for a safe one.
printf '{"tool_name":"Bash","tool_input":{"command":"gh pr merge 1"}}' \
  | bash plugins/assembly/hooks/ask-first-guard.sh
printf '{"tool_name":"Bash","tool_input":{"command":"npm install"}}' \
  | bash plugins/assembly/hooks/ask-first-guard.sh

# SessionStart: prints a primer when .agents/status.md exists, nothing otherwise.
CLAUDE_PROJECT_DIR="$PWD" bash plugins/assembly/hooks/session-start.sh
```

## Manual Acceptance Checklist

- [ ] Only the 13 public skills are triggerable from this plugin.
- [ ] `next` dispatches to the next evidence-backed action and does not guess when status is ambiguous.
- [ ] `project-status` handles scaffold, status, and repair without separate `new-project` or `introspect` skills.
- [ ] Scaffolds keep agent-only operating files under `.agents/` and do not create `docs/agent-guidance.md`.
- [ ] Force-scaffolding a subproject preserves existing `.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, and `reference/README.md`, and appends to `.agents/log.md`.
- [ ] `product-discovery` is interview-first and makes product calls only when delegated or strongly supported by project evidence.
- [ ] Empty or minimal `build` prompts infer and execute the first unambiguous build-track gate instead of stopping for a named task.
- [ ] Public skills load references conditionally and do not name deleted support skills as dependencies.
- [ ] `plugins/assembly/scripts/audit_skill_conflicts.py` reports local overlapping lifecycle skills.
- [ ] Missing phase prerequisites produce a warning and double-back skill recommendation.
- [ ] Material GitHub-backed work uses `gh` for a descriptive PR handoff, deciding draft vs ready as an engineering call.
- [ ] PRs are promoted to ready autonomously once reviewer sub-agents are satisfied and verification is green — no founder approval required.
- [ ] Merge and deploy proceed autonomously when `Traffic state: pre-live`; when `live`, the agent asks the founder GO/NO-GO before merging to the default branch, then deploy follows.
- [ ] Existing PR branches use idempotent branch switching and `gh pr edit` rather than create-only flows.
- [ ] Blocked GitHub handoff reports the blocker, local work, verification status, and recovery step instead of looping.
- [ ] PR review comments are addressed with thread-aware reads, pushed fixes, and autonomous replies/resolution; only product/UX threads escalate to the founder.
