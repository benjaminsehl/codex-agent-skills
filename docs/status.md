# Project Status: Assembly

Last updated: 2026-06-04
Current phase: proposal
Traffic state: pre-live

<!-- assembly:status — machine-readable mirror of the prose below.
     Humans read the sections; tools, CI, and external operators read this block.
     Keep it in sync with the prose; validate_status.py checks its shape. -->

```yaml
schema: assembly-status/v1
project: assembly
phase: proposal
current_gate: founder-prioritization-capability-assembly-vs-stage-0
next_skill: build
traffic_state: pre-live
blocked: false
needs_founder_input: true
last_verified: 2026-06-04
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
```

## Autonomy

- Traffic state: pre-live. Assembly is not yet depended on by real users, so agents run the roadmap autonomously — open PRs, run reviewer sub-agents, merge, and (where a deploy path exists) deploy — escalating only product/UX decisions and always-ask floor items. Flip to `live` when external builders depend on the published plugin and you want merging to the default branch to become a founder GO/NO-GO (deploy then follows the approved merge).
- Escalation model defined in `docs/decisions/2026-05-29-autonomy-escalation-model.md` and `plugins/assembly/references/agent-operating-protocol.md`.

## Phase Verdict

- Current phase: proposal
- Why: Assembly now installs and loads as a working plugin in both Codex and Claude Code, and the product direction is sharper: Assembly 1.0 proves the human-led control loop for an eventual agentic app factory across both runtimes; a post-1.0 orchestrator becomes the next step only after the loop is reliable.
- Evidence: PR #1 merged the project-workflow foundation into `main`; PR #2 merged as `15cb36a`; PR #4 added dual-runtime support via `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, and validator/audit-script updates; Assembly `0.8.3` is installed under `~/.codex/plugins/cache/assembly/assembly/0.8.3`; `docs/specs/assembly-1-0.md` defines the 1.0 behavior spec; `docs/product/app-factory-north-star.md`, `docs/research/2026-05-27-agentic-orchestration-research.md`, `docs/plans/2026-05-27-assembly-1-0-release-plan.md`, and `docs/plans/2026-05-27-post-1-0-orchestrator-roadmap.md` now capture the north star, research synthesis, release path, and post-1.0 roadmap.
- Structure decision: agent-only operating files now belong under `.agents/`, with root `AGENTS.md` as the visible entrypoint and `reference/` reserved for raw source material.
- Product decision: 1.0 ships as a dual-runtime plugin (Codex + Claude Code) from the same bundle and must pass install/smoke checks in both runtimes; post-1.0 orchestration is the next strategic direction. See `docs/decisions/2026-05-27-dual-runtime-claude-code.md`.
- Product-intent completeness: what is being built, why it matters, and what good looks like are now explicit in the spec and north-star docs.
- Next gate: founder review/acceptance of `docs/specs/assembly-1-0.md`, then `plan` for release-candidate implementation and proof tasks.

## Next Recommended Skills

- `plan` (break Stage 0 of the 10x roadmap into slices)
- `build`

## 10x Direction (accepted 2026-06-01)

Founder accepted a measurement-first 10x direction across all four axes (output
quality, product-vision alignment, code coherence, autonomous operations). The
core thesis: Assembly is open-loop and the founder is the only sensor on every
axis; 10x closes four instrumented loops, sequenced so autonomy scales only as
fast as measured quality, alignment, and coherence allow.

The measurement substrate has two tracks: a sparse, founder-authored
course-correction ledger (`docs/evals/course-corrections/`) for product
direction, and agent-graded quality evals (rubrics + fixtures) for code the
founder will not review. Scope is Ben's personal stack; "ship 1.0" is not a
blocking gate — do the most important thing at any moment.

- Roadmap: `docs/plans/2026-06-01-assembly-10x-roadmap.md`
- Decision: `docs/decisions/2026-06-01-measurement-first-10x.md`

## New Thread: Capability Assembly (captured 2026-06-02)

Founder ideation captured as a discovery brief: a thin capability-assembly step
that composes skills.sh's `find-skills` to load the best domain skills for a
project's stack (e.g. `cloudflare/skills` for a Cloudflare project) and records
them in `AGENTS.md` so every session leverages them. This is a **new axis —
capability acquisition** — distinct from the four measurement loops of the 10x
roadmap; recorded as its own thread, not yet specced.

- Brief: `docs/product/discovery-capability-assembly.md`
- Spec: `docs/specs/capability-assembly.md` (accepted 2026-06-04; merged via PR #15).
- Plan: `tasks/plan.md` (PR #17) — 4 dependency-ordered tasks + 2 checkpoints (stack detection → `assemble` skill incl. persistence + surface 13→14 → `init` integration → boundaries/smoke). Stage 0's status block (PR #14) resolved the prior persistence dependency. **Founder decision pending** (see Next Concrete Action): accept the plan and choose whether this or finishing Stage 0's eval-harness is the next build slice.

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

Two open threads; which is the next build slice is a founder prioritization call
(`needs_founder_input: true` above):

1. **Capability assembly** — accept `tasks/plan.md` (PR #17), then `build` T1
   (stack detection: `detect_stack.py` + signal reference).
2. **Stage 0 eval harness** — the remaining Stage 0 slice of
   `docs/plans/2026-06-01-assembly-10x-roadmap.md`: an eval-harness skeleton (a
   runner, the rubric file format, and 1–2 fixtures). Stage 0's other pieces (CI,
   the machine-readable status block, `validate_status.py`) shipped in PR #14.

The earlier 1.0 release-plan work
(`docs/plans/2026-05-27-assembly-1-0-release-plan.md`) is not abandoned but is no
longer a blocking gate — pursue whatever is most important at the moment.
