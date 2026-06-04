# Plan: Capability Assembly (`assemble`)

Last updated: 2026-06-02
Status: draft for review
Spec: `docs/specs/capability-assembly.md`
Discovery: `docs/product/discovery-capability-assembly.md`

## Scope being planned

Implement the `assemble` skill from the accepted spec: detect a project's stack,
discover skills via skills.sh's `find-skills`/`npx skills`, verify reputation
before installing, auto-install verified matches, and persist the set to both the
`AGENTS.md` "Capabilities" section and the machine-readable status block. Wire it
into `init`.

## What changed since the spec

- **Stage 0 landed (PR #14).** The machine-readable status block (`assembly-status/v1`)
  and `validate_status.py` now exist, with CI running the validators on every PR.
  The spec's "status-block half depends on Stage 0" dependency is **resolved** —
  this plan implements both persistence surfaces.
- `validate_status.py` requires a fixed set of top-level keys but **allows extra
  keys**, so adding a `capabilities` field to the v1 block needs no validator
  change (we extend it only to shape-check the new field, optionally).
- `validate_skill_graph.py` enforces an allowlist (`SKILL_REFERENCES`), caps each
  public skill at **120 lines**, and forbids `## Underlying skills`. Registering
  `assemble` must update that allowlist and keep the skill body thin.

## Engineering choices (autonomous; flag if you disagree)

- **Stack detection ships as a small `scripts/detect_stack.py`** returning JSON
  (`{stack, signals}`), not pure skill instructions — deterministic, testable, and
  reusable by `init`. The skill owns the confirm-before-search interaction layer.
- **Install/verification stays in the skill body** (it drives `npx skills`), not a
  script, since it is an interactive, judgment-bearing step.

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

### T2 — `assemble` skill (full behavior incl. persistence) + surface registration (13 → 14)

> **Sequencing (review #17, comment #4):** the moment
> `plugins/assembly/skills/assemble/SKILL.md` exists it must be in the
> `validate_skill_graph.py` allowlist or CI fails ("unexpected triggerable
> skills") — Assembly has no "private skill" state. So the green slice that
> exposes `assemble` must already persist; persistence is folded into this task,
> not deferred to a later one. The first public version is spec-complete.

- **Acceptance:** `plugins/assembly/skills/assemble/SKILL.md` (≤120 lines, no
  `## Underlying skills`) implements detect → confirm → `npx skills find` → verify
  reputation (install count / source / stars) → auto-install verified via
  `npx skills add` → report → **persist to both the `AGENTS.md` "Capabilities"
  section and the `assembly-status/v1` `capabilities:` list**, reconciling (no
  duplicates, founder-authored entries preserved). Below-bar matches listed, never
  auto-installed. The 14-skill surface passes all validators, and every
  surface-enumerating doc lists `assemble`.
- **Verify:** `validate_skill_graph.py`, `audit_skill_conflicts.py`,
  `validate_plugin.py`, `validate_status.py` all green; a documented dry-run shows
  reconcile (no duplicates, founder entry preserved); grep shows `assemble` across
  the surface docs.
- **Files:**
  - `plugins/assembly/skills/assemble/SKILL.md` (new)
  - `plugins/assembly/scripts/validate_skill_graph.py` (`SKILL_REFERENCES` allowlist)
  - `plugins/assembly/scripts/audit_skill_conflicts.py`
  - `plugins/assembly/templates/AGENTS.md` (Capabilities section) + `plugins/assembly/scripts/scaffold_project.py` (seed it)
  - `docs/status.md` (`capabilities: []` in the block); optionally `plugins/assembly/scripts/validate_status.py` (shape-check the field)
  - surface docs: `README.md`, `plugins/assembly/skills/README.md`, `plugins/assembly/docs/SPEC.md`, `plugins/assembly/docs/COMMAND_CONTRACT.md`, `plugins/assembly/docs/INSTALL.md`, `docs/specs/assembly-1-0.md` (candidate set 13 → 14)
- **Depends on:** T1.

> **Checkpoint A:** `assemble` is public *and spec-complete* — detect → find →
> verify → install → persist to both surfaces — with CI green. No half-exposed
> workflow that installs without recording.

### T3 — `init` integration
- **Acceptance:** `init` invokes `assemble` after scaffold when `detect_stack.py`
  finds a stack, or recommends it as the next step when the stack is unclear.
- **Verify:** `validate_skill_graph.py` green (init still thin);
  `plugins/assembly/skills/init/SKILL.md` references `assemble`; SMOKE_TESTS note
  describes the init → assemble handoff.
- **Files:** `plugins/assembly/skills/init/SKILL.md`, `plugins/assembly/docs/SMOKE_TESTS.md`.
- **Depends on:** T2.

> **Checkpoint B:** end-to-end — scaffold a Cloudflare-style fixture, `init` hands
> to `assemble`, which detects, confirms, installs verified skills, and records
> them in both surfaces.

### T4 — Boundaries, failure modes, smoke evidence
- **Acceptance:** the skill encodes always/ask-first/never from the spec (verify
  before install; ask-first when a below-bar skill ships scripts/hooks; never
  install unverified or overwrite founder entries) and fails clearly when
  `npx skills`/Node is absent rather than half-acting. A smoke entry proves a real
  run end to end.
- **Verify:** full validator suite green; `python3 -m py_compile` on all scripts;
  SMOKE_TESTS run recorded.
- **Files:** `plugins/assembly/skills/assemble/SKILL.md`, `plugins/assembly/docs/SMOKE_TESTS.md`,
  `plugins/assembly/references/agent-operating-protocol.md` (if a floor line is
  needed).
- **Depends on:** T2–T3.

## Open questions carried from spec (resolve during build)

- Reputation thresholds: adopt `find-skills` defaults (≈1K installs; distrust
  <100-star repos) as-is for v1, tune later. **Lean: adopt as-is.**
- Status-block capability fields: `name`, `source`, `version`/commit, `installed_at`?
- Multi-stack ambiguity presentation in the confirm step.
- Reconciliation when an installed skill is deprecated/removed upstream.

## Out of scope (unchanged from spec)

MCP servers and doc sources as capabilities; any new registry/ranking/install
machinery; lockfile/vendor apparatus; runtimes beyond Codex and Claude Code.

## Note on size

Four tasks with two checkpoints. T2 is deliberately the largest: per review #17
(comment #4), exposing `assemble` publicly and persisting its results must ship in
the same green slice, since Assembly has no "private skill" state. T2 can be
delivered as stacked commits, but it lands as one CI-green unit so no half-exposed
workflow is ever merged.
