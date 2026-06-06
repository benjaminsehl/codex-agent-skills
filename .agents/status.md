# Project Status: Assembly

Last updated: 2026-06-06
Current phase: proposal
Traffic state: pre-live

<!-- assembly:status — machine-readable mirror of the prose below.
     Humans read the sections; tools, CI, and external operators read this block.
     Keep it in sync with the prose; validate_status.py checks its shape. -->

```yaml
schema: assembly-status/v1
project: assembly
phase: proposal
current_gate: capability-assembly-live-smoke
next_skill: qa
traffic_state: pre-live
blocked: false
needs_founder_input: true
last_verified: 2026-06-06
autonomy:
  product_decisions: founder      # always escalate, in product-implication language
  engineering_decisions: agent    # autonomous, validated by reviewer sub-agents
  merge: autonomous               # pre-live; founder GO/NO-GO when traffic_state is live
  deploy: autonomous              # follows the approved merge
verification:
  ci: .github/workflows/validate.yml
  validators:
    - python3 plugins/assembly/scripts/validate_plugin.py
    - python3 plugins/assembly/scripts/validate_skill_graph.py
    - python3 plugins/assembly/scripts/validate_status.py
    - python3 plugins/assembly/scripts/audit_skill_conflicts.py
escalation_floor:                 # never autonomous, in any traffic state
  - money-movement
  - credentials-or-secrets
  - external-messaging
  - privacy-sensitive-data
  - irreversible-destructive-ops
  - merge-to-default-when-live
capabilities: []                  # domain skills assembled for the stack; see references/capability-acquisition.md
```

## Autonomy

- Traffic state: pre-live. Assembly is not yet depended on by real users, so agents run the roadmap autonomously — open PRs, run reviewer sub-agents, merge, and (where a deploy path exists) deploy — escalating only product/UX decisions and always-ask floor items. Flip to `live` when external builders depend on the published plugin and you want merging to the default branch to become a founder GO/NO-GO (deploy then follows the approved merge).
- Escalation model defined in `docs/decisions/2026-05-29-autonomy-escalation-model.md` and `plugins/assembly/references/agent-operating-protocol.md`.

## Phase Verdict

- Current phase: proposal
- Why: Assembly now installs and loads as a working plugin in both Codex and Claude Code, and the product direction is sharper: Assembly 1.0 proves the human-led control loop for an eventual agentic app factory across both runtimes; a post-1.0 orchestrator becomes the next step only after the loop is reliable.
- Evidence: PR #1 merged the project-workflow foundation into `main`; PR #2 merged as `15cb36a`; PR #4 added dual-runtime support via `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and validator/audit-script updates; Assembly `0.8.3` is installed under `~/.codex/plugins/cache/assembly/assembly/0.8.3`; `.agents/specs/assembly-1-0.md` defines the 1.0 behavior spec; `docs/product/app-factory-north-star.md`, `.agents/research/2026-05-27-agentic-orchestration-research.md`, `.agents/plans/2026-05-27-assembly-1-0-release-plan.md`, and `.agents/plans/2026-05-27-post-1-0-orchestrator-roadmap.md` now capture the north star, research synthesis, release path, and post-1.0 roadmap.
- Structure decision: agent-only operating files now belong under `.agents/`, with root `AGENTS.md` as the visible entrypoint and `reference/` reserved for raw source material.
- Product decision: 1.0 ships as a dual-runtime plugin (Codex + Claude Code) from the same bundle and must pass install/smoke checks in both runtimes; post-1.0 orchestration is the next strategic direction. See `docs/decisions/2026-05-27-dual-runtime-claude-code.md`.
- Product-intent completeness: what is being built, why it matters, and what good looks like are now explicit in the spec and north-star docs.
- Next gate: capability assembly is built and merged (T1–T3) with T4's boundaries/failure-modes done and the live smoke *procedure* documented (`plugins/assembly/docs/SMOKE_TESTS.md`). The one remaining step is the founder running the **recorded end-to-end smoke run** in a live `npx skills` environment (`needs_founder_input: true`). With the capability-assembly build essentially complete, the deliberately *separate, parallel* measurement-first 10x axis is the next dev work: its Stage 0 eval-harness slice. Founder review/acceptance of `.agents/specs/assembly-1-0.md` remains open but non-blocking. Two-axis relationship and priority: `docs/decisions/2026-06-06-two-axes-capability-and-measurement.md`.

## Next Recommended Skills

- `qa` (run the documented capability-assembly live smoke procedure in a real `npx skills` env, then record evidence in `.agents/qa/`)
- `build`/`plan` for the Stage 0 eval-harness slice of the measurement axis (the next dev work now that the capability build is complete)

## 10x Direction (accepted 2026-06-01)

Founder accepted a measurement-first 10x direction across all four axes (output
quality, product-vision alignment, code coherence, autonomous operations). The
core thesis: Assembly is open-loop and the founder is the only sensor on every
axis; 10x closes four instrumented loops, sequenced so autonomy scales only as
fast as measured quality, alignment, and coherence allow.

The measurement substrate has two tracks: a sparse, founder-authored
course-correction ledger (`.agents/evals/course-corrections/`) for product
direction, and agent-graded quality evals (rubrics + fixtures) for code the
founder will not review. Scope is Ben's personal stack; "ship 1.0" is not a
blocking gate — do the most important thing at any moment.

- Roadmap: `.agents/plans/2026-06-01-assembly-10x-roadmap.md`
- Decision: `docs/decisions/2026-06-01-measurement-first-10x.md`

## New Thread: Capability Assembly (captured 2026-06-02)

Founder ideation captured as a discovery brief: a thin capability-assembly step
that composes skills.sh's `find-skills` to load the best domain skills for a
project's stack (e.g. `cloudflare/skills` for a Cloudflare project) and records
them in `AGENTS.md` so every session leverages them. This is a **new axis —
capability acquisition** — distinct from the four measurement loops of the 10x
roadmap; recorded as its own thread, not yet specced.

- Brief: `docs/product/discovery-capability-assembly.md`
- Spec: `.agents/specs/capability-assembly.md` (accepted; design revised 2026-06-04 after a design tournament).
- Design (decided 2026-06-04): a **shared capability-acquisition behavior**, not a new skill — `init` seeds it, `build` fires it just-in-time (task-scoped), `project-status` re-runs it. Public surface stays at 13. A 5-approach tournament found the original 14th-skill design was a strong #2 that paid an avoidable surface tax; the founder adopted the hybrid.
- Plan: `tasks/plan.md` — T1–T3 merged (PRs #18/#19/#20); T4 boundaries/failure-modes done and the live smoke procedure documented. Only the founder-run recorded live-smoke evidence remains.

## Current 1.0 Direction

- Candidate wedge: install Assembly, scaffold a repo, say `next`, and have Codex orient to phase, missing context, and the next useful workflow without guessing or silently taking product authority.
- Primary user: Ben acting as founder/product director while agents help clarify, execute, verify, and preserve the project trail.
- Secondary user: people who want a compact Codex-native product-building workflow instead of a pile of overlapping skills.
- Default stance: optimize 1.0 as Ben's personal stack first, built in public so other builders can adopt it if they want; they are not the audience 1.0 is designed around.
- Recommended proof path: Assembly self-hosts the workflow, CFO proves a greenfield/restart setup, and Hyper remains the richer retrofit proof or release stretch.
- Post-1.0 north star: a post-1.0 orchestrator coordinates scoped agent sessions using Assembly's project trail, phase gates, and GitHub handoff loop.
- Latest usage feedback: `product-discovery` should interview before deciding unless delegated; empty or minimal `build` prompts should infer and execute the first unambiguous build-track gate.

## 1.0 Open Questions

- Founder acceptance: is the 1.0 spec and north-star framing right?
- CFO proof scope: how much should the proof mutate `/Users/sai/cfo` versus inspect and report first?
- Release-candidate timing: should Hyper retrofit stay stretch, or become blocking after CFO?

## Next Concrete Action

Capability assembly is **built and merged** (hybrid behavior, surface stays 13):
T1 stack detection, T2 shared behavior + dual persistence, T3 wired into `init` /
`build` / `project-status`. T4's boundaries and failure-handling are in
`references/capability-acquisition.md`, and the live smoke **procedure** is
documented in `plugins/assembly/docs/SMOKE_TESTS.md`.

The one remaining step is **founder-run**: execute that recorded end-to-end smoke
run in a real `npx skills` environment (the sandbox has no registry/network) and
drop the evidence in `.agents/qa/`. That closes Checkpoint B and T4.

Parallel open item, not blocking: the remaining **Stage 0 eval-harness** slice of
`.agents/plans/2026-06-01-assembly-10x-roadmap.md` (a runner, the rubric file format,
1–2 fixtures); Stage 0's other pieces shipped in PR #14. The earlier 1.0
release-plan work is not abandoned but is no longer a blocking gate — pursue
whatever is most important at the moment.
