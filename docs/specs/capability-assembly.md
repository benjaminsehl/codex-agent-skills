# Spec: Capability Assembly (`assemble`)

Last updated: 2026-06-04
Status: accepted (founder, 2026-06-04); planned in `tasks/plan.md` (PR #17)
Signal density: lightweight (fresh discovery in `docs/product/discovery-capability-assembly.md`), extended with behavior requirements and boundaries because it introduces a new public skill.
Discovery: `docs/product/discovery-capability-assembly.md`

## Objective

Add a thin capability-assembly step to Assembly so that, for a project's known
stack, the agent discovers and installs the best domain skills and records them
durably — making per-domain competence a property of the project rather than of
whoever prompted well in a given session.

Assembly composes skills.sh's existing
[`find-skills`](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)
and `npx skills` CLI for discovery, ranking, and install; the new work Assembly
owns is stack detection, verification-gated installation, and durable persistence
into the project trail.

## User And Pain

Primary user: Ben building real apps with agents across varied stacks (Cloudflare,
Vercel, etc.). The painful moment, current workarounds, and lovable moment are in
the discovery brief. In short: today the agent improvises platform behavior with no
domain skill loaded; `assemble` makes the right skills travel with the project.

## Mini-Discovery Decisions (founder, 2026-06-02)

These four founder answers shape the spec:

1. **Skill surface** — ship a new public skill **`assemble`** (14th skill). `init`
   invokes it on scaffold; the founder re-invokes it whenever the stack grows.
2. **Stack input** — **sniff the repo, then confirm.** Infer the stack from repo
   signals, show what was inferred, and let the founder confirm/adjust before
   searching. No silent action on a guess.
3. **Source of truth** — **both.** A human-readable `AGENTS.md` "Capabilities"
   section *and* a machine-readable entry in the status block (the YAML block from
   Stage 0 of the 10x roadmap), so humans and tooling/orchestrator both read it.
4. **Install gate** — **auto-install verified matches.** Matches that clear the
   reputation bar install autonomously and are reported; this matches pre-live
   autonomy. The always-ask floor still applies.

## Scope

A new public skill `assemble` that:

- Detects the project's stack from repo signals, presents the inference, and
  confirms with the founder before searching.
- Discovers candidate skills via `find-skills` / `npx skills find <stack queries>`
  against the skills.sh registry.
- **Verifies reputation before installing** — install count, source-repo
  reputation, and GitHub stars — per the `find-skills` contract. Never installs
  from search results alone.
- Auto-installs matches that clear the reputation bar via `npx skills add`, and
  reports each one (name, source, install count/stars, why it was chosen).
- Lists matches that do *not* clear the bar as optional candidates; never installs
  them automatically.
- Persists the assembled set to both the `AGENTS.md` "Capabilities" section and the
  machine-readable status block.
- Is idempotent: re-running reconciles the existing Capabilities list instead of
  duplicating entries.
- Is invoked by `init` on scaffold and is re-invocable standalone when the stack
  grows (new subproject, new platform).

## Behavior Requirements

### `assemble`

`assemble` must:

- State that the `assemble` workflow is active and name the target project/subproject scope.
- Detect stack from a seed signal set (e.g. `wrangler.toml`/`wrangler.jsonc` → Cloudflare, `package.json` deps, `next.config.*`, framework/config markers), present the inferred stack, and wait for founder confirmation or correction before searching.
- Run `npx skills find` with stack-derived queries and apply the `find-skills` verification step (install count, source reputation, GitHub stars) **before** any install.
- Auto-install only matches that clear the reputation bar; install via `npx skills add`; report each install with name, source, reputation signals, and rationale.
- Surface below-bar or niche matches as optional candidates the founder can opt into — never auto-install them.
- Flag when an about-to-be-installed skill ships executable scripts/hooks (not just instructions) in its report, so the founder sees it.
- Write/reconcile the `AGENTS.md` "Capabilities" section: one entry per assembled skill (name, source, why), preserving any founder-authored entries.
- Write/reconcile the machine-readable status-block capability list when that block exists; degrade to AGENTS.md-only until it lands.
- Append a one-line entry to `.agents/log.md` naming what was assembled.
- Work in both Codex and Claude Code; if `npx skills` (Node) is unavailable, stop with a clear message naming the missing dependency rather than half-acting.

### `init` integration

- `init` invokes `assemble` after scaffold once a stack is detectable, or recommends it as the next step when the stack is not yet clear.

## Out Of Scope

- Assembling **MCP servers** and **doc sources** as capabilities — the seam is
  acknowledged (Cloudflare reaches a session as MCP + docs, not a skill bundle),
  but v1 is skills-only.
- Building any registry, ranking, or install machinery — composed from `find-skills` / `npx skills`.
- A lockfile/vendor/security-auditor apparatus — not needed for the wedge (see discovery brief); the reputation verification step is the line.
- Runtimes other than Codex and Claude Code.

## Dependencies And Sequencing

- **Status-block half depends on Stage 0** of `docs/plans/2026-06-01-assembly-10x-roadmap.md` (the machine-readable YAML status block). `assemble` can ship the `AGENTS.md` half now and wire the status-block half when the block lands; this is a dependency, not a blocker.
- **Public surface change (13 → 14 skills).** Adding `assemble` requires updating `plugins/assembly/.claude-plugin/plugin.json`, the Codex manifest, the marketplace, `audit_skill_conflicts.py`, `validate_skill_graph.py`, and the candidate skill set in `docs/specs/assembly-1-0.md`. This is the founder-approved surface decision from mini-discovery.
- **`npx skills` availability** in the execution environment (Node) is an external runtime dependency.

## Boundaries

### Always

- Run the reputation verification step before any install.
- Report every installed skill with its source and reputation signals.
- Preserve founder-authored entries when reconciling the Capabilities section.

### Ask first

- Anything on the always-ask floor (credentials, external messaging, irreversible/destructive ops).
- Installing a skill that ships executable scripts/hooks when it is below the reputation bar.

### Never

- Install a skill from search results without verification.
- Auto-install below-bar/niche matches.
- Overwrite or drop a founder-authored Capabilities entry during reconciliation.

## Assumptions

- The `find-skills` defaults are a reasonable reputation bar to start (prefer ~1K+ installs; treat <100-star source repos with skepticism), tunable later.
- A small seed of stack-detection signals covers the near-term stacks (Cloudflare, Vercel/Next, common Node frameworks); the set grows from use.
- Skills are predominantly instructions; the scripts/hooks caveat is handled by the verification bar plus the report flag, not heavier machinery.

## Success Criteria

- Running `assemble` in a repo with a detectable stack shows the inferred stack, takes founder confirmation, and produces a verified, reported install set.
- No skill is installed without the reputation verification step appearing in the run trace.
- Each auto-installed skill appears in the `AGENTS.md` "Capabilities" section with name, source, and rationale.
- Re-running `assemble` reconciles rather than duplicates entries, and preserves founder-authored entries.
- Below-bar matches are listed as candidates, not installed.
- `init` invokes or recommends `assemble` on scaffold.
- The skill behaves in both Codex and Claude Code, and fails clearly when `npx skills` is unavailable.

## Open Questions

- Exact reputation thresholds: adopt `find-skills` defaults as-is, or tune the install-count/star floors?
- Status-block schema: what capability fields does the Stage 0 YAML block carry (name, source, version/commit, installed-at)?
- Stack-detection seed set: which signals ship in v1, and how is ambiguity (multi-stack repos) presented?
- Reconciliation UX when an installed skill is deprecated or removed upstream on a later `assemble` run.

## Recommended Next Step

Done: planned in `tasks/plan.md` (PR #17) as four dependency-ordered tasks
(stack detection → `assemble` skill incl. persistence + surface registration →
`init` integration → boundaries/smoke). Stage 0 (PR #14) shipped the
machine-readable status block, so the status-block persistence is no longer a
deferred dependency. Next: `build` T1 once the founder picks the next slice.
