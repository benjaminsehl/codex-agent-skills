# Plan: Capability Assembly (behavior)

Last updated: 2026-06-04
Status: draft for review
Spec: `docs/specs/capability-assembly.md`
Discovery: `docs/product/discovery-capability-assembly.md`

## Scope being planned

Implement capability assembly per the **hybrid** design (spec revised 2026-06-04
after a design tournament): a shared capability-acquisition *behavior* — not a new
skill — that detects a project's stack, discovers skills via skills.sh's
`find-skills`/`npx skills`, verifies reputation before installing, auto-installs
verified matches, and persists the set to both the `AGENTS.md` "Capabilities"
section and the `assembly-status/v1` `capabilities:` list. It is wired into three
existing call sites: `init`, `build`, and `project-status`. The public skill
surface stays at 13.

## What changed (design tournament, 2026-06-04)

- The pivot from a 14th `assemble` skill to a shared behavior **deletes the entire
  surface-registration task** (no allowlist / audit / marketplace / Codex-manifest
  / 6-doc edits). The net plan is smaller and lower-risk than the A1 version.
- **Stage 0 (PR #14)** already shipped the `assembly-status/v1` block and
  `validate_status.py`. The validator allows extra top-level keys, so a
  `capabilities:` field is additive — no validator change required (we may extend
  it to shape-check the field, optionally).
- `validate_skill_graph.py` caps each public skill at **120 lines** and forbids
  `## Underlying skills`. The call-site edits to `init`/`build`/`project-status`
  must keep those skills thin and point at the shared reference rather than inlining
  the procedure.

## Engineering choices (autonomous; flag if you disagree)

- **Stack detection ships as a small `detect_stack.py`** returning JSON
  (`{stack, signals}`) — deterministic, testable, reusable by every call site.
- **The acquisition procedure lives in one shared reference**
  (`references/capability-acquisition.md`); the three call sites invoke it in a few
  lines each, so logic is single-sourced (no copy-paste drift) and the skill bodies
  stay thin.

## Tasks (dependency-ordered)

### T1 — Stack detection (`detect_stack.py` + signal reference)
- **Acceptance:** `detect_stack.py --root <path>` emits JSON naming the inferred
  stack(s) and the signals matched, from a seed set (Cloudflare via
  `wrangler.toml`/`wrangler.jsonc`; Next/Vercel via `next.config.*` + deps; common
  Node frameworks via `package.json`). Multi-stack repos return all matches.
  A `references/stack-signals.md` documents the seed set and how to extend it.
- **Verify:** `python3 plugins/assembly/scripts/detect_stack.py --root <fixture>`
  on a Cloudflare-style fixture prints `cloudflare`; `python3 -m py_compile` passes.
- **Files:** `plugins/assembly/scripts/detect_stack.py` (new),
  `plugins/assembly/references/stack-signals.md` (new),
  `plugins/assembly/scripts/README.md`, CI py_compile list in
  `.github/workflows/validate.yml`.
- **Depends on:** none.

### T2 — Shared capability-acquisition behavior + persistence
- **Acceptance:** `plugins/assembly/references/capability-acquisition.md` defines
  the full procedure: detect → confirm → `npx skills find` → verify reputation
  (install count / source / stars) → auto-install verified via `npx skills add` →
  report → **persist to both the `AGENTS.md` "Capabilities" section and the
  `assembly-status/v1` `capabilities:` list**, reconciling (no duplicates,
  founder-authored entries preserved). Below-bar matches listed, never
  auto-installed. The `capabilities:` field is added to the status block; the
  `AGENTS.md` template gains the Capabilities section and scaffold seeds it.
- **Verify:** `validate_status.py` green with a sample `capabilities` entry;
  `validate_skill_graph.py`, `validate_plugin.py`, `audit_skill_conflicts.py`
  still green (surface unchanged at 13); a documented dry-run shows reconcile (no
  duplicates, founder entry preserved).
- **Files:**
  - `plugins/assembly/references/capability-acquisition.md` (new)
  - `plugins/assembly/templates/AGENTS.md` (Capabilities section) + `plugins/assembly/scripts/scaffold_project.py` (seed it)
  - `docs/status.md` (`capabilities: []` in the block); optionally `plugins/assembly/scripts/validate_status.py` (shape-check the field)
- **Depends on:** T1.

> **Checkpoint A:** the shared behavior is spec-complete (detect → find → verify →
> install → persist to both surfaces), persistence validates, and the public
> surface is unchanged at 13. No new skill registered.

### T3 — Call-site wiring (`init`, `build`, `project-status`)
- **Acceptance:**
  - `init` runs the behavior (stack-scoped) after scaffold when a stack is
    detectable, else recommends it.
  - `build` fires the behavior just-in-time with a **task-scoped** query when a
    slice touches platform behavior with no loaded skill — an explicit boundary
    clause, not a silent self-check.
  - `project-status` exposes an explicit "re-assemble capabilities" route for when
    the stack grows.
- **Verify:** `validate_skill_graph.py` green (all three skills still thin, ≤120
  lines, no `## Underlying skills`); each SKILL.md references
  `capability-acquisition.md`; SMOKE_TESTS note describes the handoffs.
- **Files:** `plugins/assembly/skills/init/SKILL.md`,
  `plugins/assembly/skills/build/SKILL.md`,
  `plugins/assembly/skills/project-status/SKILL.md`,
  `plugins/assembly/docs/SMOKE_TESTS.md`.
- **Depends on:** T2.

> **Checkpoint B:** end-to-end — scaffold a Cloudflare-style fixture; `init`
> acquires stack skills; a `build` slice triggers a task-scoped acquisition;
> `project-status` re-runs it; all recorded in both surfaces, surface still 13.

### T4 — Boundaries, failure modes, smoke evidence
- **Acceptance:** the shared reference encodes always/ask-first/never from the spec
  (verify before install; ask-first when a below-bar skill ships scripts/hooks;
  never install unverified or overwrite founder entries) and fails clearly when
  `npx skills`/Node is absent rather than half-acting. A smoke entry proves a real
  run end to end.
- **Verify:** full validator suite green; `python3 -m py_compile` on all scripts;
  SMOKE_TESTS run recorded.
- **Files:** `plugins/assembly/references/capability-acquisition.md`,
  `plugins/assembly/docs/SMOKE_TESTS.md`,
  `plugins/assembly/references/agent-operating-protocol.md` (if a floor line is
  needed).
- **Depends on:** T2–T3.

## Open questions carried from spec (resolve during build)

- Reputation thresholds: adopt `find-skills` defaults (≈1K installs; distrust
  <100-star repos) as-is for v1, tune later. **Lean: adopt as-is.**
- Status-block capability fields: `name`, `source`, `version`/commit, `installed_at`?
- Multi-stack ambiguity presentation in the confirm step.
- `build` trigger wording: fires reliably without becoming per-slice noise.
- Reconciliation when an installed skill is deprecated/removed upstream.

## Out of scope (unchanged from spec)

MCP servers and doc sources as capabilities; any registry/ranking/install
machinery; a declarative manifest/reconcile engine; lockfile/vendor apparatus;
runtimes beyond Codex and Claude Code.

## Note on size

Four tasks, two checkpoints — smaller than the pre-tournament A1 plan, which spent
a whole task registering a 14th skill across ~7 files. The hybrid keeps the surface
at 13, so T2 is "write one reference + the persistence field" and T3 is three thin
call-site edits. No half-exposed-skill hazard, because no skill is registered.
