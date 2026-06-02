# Agent Log

Append meaningful agent handoff events, skipped gates, recovery notes, and project-operation changes here.

## 2026-05-22

- Scaffolded Assembly's root project trail under `docs/`.
- Added GitHub handoff guidance for focused commits, draft PRs, self-review, simplification, and ready-for-review gates.
- Moved agent-only operating material under `.agents/` while keeping root `AGENTS.md` as the visible entrypoint.

## 2026-05-23

- Merged PR #1 into `main` at `210b3fd`, upgraded the local marketplace install to Assembly `0.8.1`, and repaired `docs/status.md` to reflect the post-merge proposal state.
- Used `next` to route into proposal-phase product discovery; recorded the recommended 1.0 stance as personal-stack-first with public installability as a quality bar.
- Recorded the product decision that Assembly 1.0 should finish the Codex plugin first; Claude support is not a near-term priority; Hermes orchestration is the post-1.0 north star.
- Captured usage feedback: `product-discovery` must ask more questions by default, and `build` with an empty/minimal prompt should infer the next build-track gate and proceed.

## 2026-05-24

- Synced `main` after PR #2 merged as `15cb36a`, verified the local Assembly marketplace bundle is already upgraded to `0.8.3`, and started the 1.0 spec branch.
- Drafted `docs/specs/assembly-1-0.md` as the Codex-first 1.0 behavior spec with Hermes orchestration captured as the post-1.0 horizon.

## 2026-06-02

- Captured founder ideation on **capability assembly** as `docs/product/discovery-capability-assembly.md`: a thin `assemble` step that composes skills.sh's `find-skills` to load the best stack-specific skills and records them in `AGENTS.md`. Framed as a new axis (capability acquisition), distinct from the 10x measurement loops. Recommended next skill: `spec` (when founder is ready). Status updated to point to the brief.
- Ran `spec` on capability assembly → `docs/specs/capability-assembly.md` (draft for review). Mini-discovery decisions: new `assemble` public skill (13→14), sniff-then-confirm stack detection, persist to both `AGENTS.md` Capabilities + machine-readable status block, auto-install verified matches (always-ask floor on top). Stopped at founder review gate; next is `plan`.

## 2026-05-27

- Used Assembly project-status/spec/plan/build flow to sharpen the 1.0 branch around a human-led agentic app factory vision.
- Added the app-factory north star, frontier orchestration research synthesis, 1.0 release plan, Hermes post-1.0 roadmap, Hermes contract draft, smoke evidence template, release checklist, and CFO proof status.
- Tightened `next`, `project-status`, and `product-discovery` so agents check what is being built, why it matters, and what good looks like before hardening product direction.
- Updated validators so the skill bodies cannot drift away from the founder/product-director and product-intent completeness requirements.
