# Spec: Capability Assembly (behavior)

Last updated: 2026-06-04
Status: accepted (founder, 2026-06-04); design revised to the hybrid below after a design tournament (2026-06-04); planned in `tasks/plan.md` (PR #17)
Signal density: lightweight (fresh discovery in `docs/product/discovery-capability-assembly.md`), extended with behavior requirements and boundaries.
Discovery: `docs/product/discovery-capability-assembly.md`

## Objective

Make per-domain competence a property of the project rather than of whoever
prompted well in a given session: for a project's stack, the agent discovers and
installs the best domain skills (e.g. `cloudflare/skills` for a Cloudflare project)
and records them durably so every future session leverages them.

Assembly composes skills.sh's existing
[`find-skills`](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)
and `npx skills` CLI for discovery, ranking, and install; the work Assembly owns is
stack detection, verification-gated installation, and durable persistence into the
project trail.

## User And Pain

Primary user: Ben building real apps with agents across varied stacks (Cloudflare,
Vercel, etc.). The painful moment, current workarounds, and lovable moment are in
the discovery brief. In short: today the agent improvises platform behavior with no
domain skill loaded; capability assembly makes the right skills travel with the
project.

## Design Revision (2026-06-04)

The original spec shipped capability assembly as a new public skill `assemble`
(the 14th). A design tournament (5 approaches, adversarial judge) found that a
dedicated skill and a shared *behavior* deliver identical machinery and identical
capability + paper-trail value, but the named skill pays an enforced surface tax
(Assembly has no "private skill" state, so a new skill dir forces allowlist +
audit + marketplace + Codex-manifest + ~6 doc edits) — ceremony against the
roadmap's named anti-goal. The founder adopted the **hybrid**: a shared behavior,
no new skill, with a named re-run handle hung off the existing `project-status`
skill. This resolves the lifecycle-placement question the discovery brief left
explicitly open; all other founder decisions below are preserved unchanged.

## Founder Decisions

1. **Surface (revised 2026-06-04)** — capability assembly is a **shared
   behavior**, not a new skill. One reference, `capability-acquisition.md`, holds
   the contract; `init` and `build` invoke it; `project-status` offers the re-run.
   The public surface stays at 13 skills.
2. **Stack input** — **sniff the repo, then confirm.** Infer the stack from repo
   signals, show what was inferred, and let the founder confirm/adjust before
   searching. No silent action on a guess.
3. **Source of truth** — **both.** A human-readable `AGENTS.md` "Capabilities"
   section *and* a machine-readable `capabilities:` list in the `assembly-status/v1`
   block, so humans and tooling/orchestrator both read it.
4. **Install gate** — **auto-install verified matches.** Matches that clear the
   reputation bar install autonomously and are reported; this matches pre-live
   autonomy. The always-ask floor still applies.

## Scope

A shared **capability-acquisition behavior** that:

- Detects the project's stack from repo signals, presents the inference, and
  confirms with the founder before searching.
- Discovers candidate skills via `find-skills` / `npx skills find <queries>`
  against the skills.sh registry.
- **Verifies reputation before installing** — install count, source-repo
  reputation, and GitHub stars — per the `find-skills` contract. Never installs
  from search results alone.
- Auto-installs matches that clear the reputation bar via `npx skills add`, and
  reports each one (name, source, install count/stars, why it was chosen).
- Lists matches that do *not* clear the bar as optional candidates; never installs
  them automatically.
- Persists the assembled set to both the `AGENTS.md` "Capabilities" section and the
  `assembly-status/v1` `capabilities:` list, idempotently (re-running reconciles
  instead of duplicating, and preserves founder-authored entries).

It is invoked at three call sites — `init` (stack-seeded on scaffold), `build`
(just-in-time when a task needs unfamiliar platform knowledge), and `project-status`
(an explicit re-run when the stack grows) — with no new public skill.

## Behavior Requirements

### Capability-acquisition behavior (shared reference)

`references/capability-acquisition.md` defines a single procedure all call sites
reuse (so logic lives in one place, not copied):

- Detect stack from a seed signal set (e.g. `wrangler.toml`/`wrangler.jsonc` →
  Cloudflare, `package.json` deps, `next.config.*`, framework/config markers),
  present the inference, and wait for founder confirmation or correction before
  searching.
- Run `npx skills find` with the appropriate queries and apply the `find-skills`
  verification step (install count, source reputation, GitHub stars) **before** any
  install.
- Auto-install only matches that clear the reputation bar via `npx skills add`;
  report each install with name, source, reputation signals, and rationale.
- Surface below-bar or niche matches as optional candidates the founder can opt
  into — never auto-install them.
- Flag when an about-to-be-installed skill ships executable scripts/hooks (not just
  instructions) in its report.
- Write/reconcile the `AGENTS.md` "Capabilities" section (one entry per skill:
  name, source, why), preserving founder-authored entries; and the
  `assembly-status/v1` `capabilities:` list.
- Append a one-line entry to `.agents/log.md` naming what was assembled.
- Work in both Codex and Claude Code; if `npx skills` (Node) is unavailable, stop
  with a clear message naming the missing dependency rather than half-acting.

### `init` call site

- After scaffold, when a stack is detectable, `init` runs the
  capability-acquisition behavior (stack-scoped); when the stack is not yet clear,
  it recommends running it as a next step.

### `build` call site (just-in-time)

- When a slice touches platform behavior the agent lacks a loaded skill for,
  `build` runs the behavior with a **task-scoped** query (e.g. "Cloudflare Durable
  Objects alarms"), not a broad stack guess — as an explicit boundary clause, not a
  silent self-assessment. It then proceeds with the acquired skill and records it.

### `project-status` re-run

- `project-status` offers an explicit "re-assemble capabilities" route for when the
  stack grows (new subproject, new platform), reusing the shared behavior. No new
  skill is added for this.

## Out Of Scope

- Assembling **MCP servers** and **doc sources** as capabilities — the seam is
  acknowledged (Cloudflare reaches a session as MCP + docs, not a skill bundle),
  but v1 is skills-only. The single shared behavior is the natural place to extend
  later.
- Building any registry, ranking, or install machinery — composed from
  `find-skills` / `npx skills`.
- A lockfile/vendor/security-auditor apparatus — not needed for the wedge (see
  discovery brief); the reputation verification step is the line.
- A declarative manifest / reconcile engine (tournament approach A3) — rejected as
  ceremony beyond the wedge.
- Runtimes other than Codex and Claude Code.

## Dependencies And Sequencing

- **No public-surface change.** The hybrid keeps the surface at 13 skills, so the
  plugin manifests, marketplace, `validate_skill_graph.py` allowlist, and
  `audit_skill_conflicts.py` are untouched. (This is the cost the design revision
  removes.)
- **Status-block persistence is unblocked.** Stage 0 (PR #14) shipped the
  `assembly-status/v1` block and `validate_status.py`; a `capabilities:` field is
  additive (the validator allows extra top-level keys), so both persistence
  surfaces ship together.
- **`npx skills` availability** in the execution environment (Node) is an external
  runtime dependency.

## Boundaries

### Always

- Run the reputation verification step before any install.
- Report every installed skill with its source and reputation signals.
- Preserve founder-authored entries when reconciling the Capabilities section.

### Ask first

- Anything on the always-ask floor (credentials, external messaging,
  irreversible/destructive ops).
- Installing a skill that ships executable scripts/hooks when it is below the
  reputation bar.

### Never

- Install a skill from search results without verification.
- Auto-install below-bar/niche matches.
- Overwrite or drop a founder-authored Capabilities entry during reconciliation.

## Assumptions

- The `find-skills` defaults are a reasonable reputation bar to start (prefer ~1K+
  installs; treat <100-star source repos with skepticism), tunable later.
- A small seed of stack-detection signals covers the near-term stacks (Cloudflare,
  Vercel/Next, common Node frameworks); the set grows from use.
- Skills are predominantly instructions; the scripts/hooks caveat is handled by the
  verification bar plus the report flag, not heavier machinery.

## Success Criteria

- Running the behavior in a repo with a detectable stack shows the inferred stack,
  takes founder confirmation, and produces a verified, reported install set.
- No skill is installed without the reputation verification step appearing in the
  run trace.
- Each auto-installed skill appears in the `AGENTS.md` "Capabilities" section and
  the status-block `capabilities:` list with name, source, and rationale.
- Re-running reconciles rather than duplicates entries, and preserves
  founder-authored entries.
- Below-bar matches are listed as candidates, not installed.
- `init` runs or recommends the behavior on scaffold; `build` fires the
  task-scoped trigger; `project-status` exposes the re-run — with the public
  surface still at 13 skills.
- The behavior works in both Codex and Claude Code, and fails clearly when
  `npx skills` is unavailable.

## Open Questions

- Exact reputation thresholds: adopt `find-skills` defaults as-is, or tune the
  install-count/star floors?
- Status-block schema: what capability fields does the `capabilities:` list carry
  (name, source, version/commit, installed-at)?
- Stack-detection seed set: which signals ship in v1, and how is ambiguity
  (multi-stack repos) presented?
- `build` trigger wording: how to phrase the boundary clause so it fires reliably
  without becoming noise on every slice.
- Reconciliation UX when an installed skill is deprecated or removed upstream.

## Recommended Next Step

Revised plan in `tasks/plan.md` (PR #17). Next: `build` T1 (stack detection —
`detect_stack.py` + signal reference), then T2 (the shared behavior + persistence,
no surface registration).
