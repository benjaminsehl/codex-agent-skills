# Product Discovery: Capability Assembly

Last updated: 2026-06-02
Status: captured (founder ideation, 2026-06-02); not yet specced
Mode: delegated on mechanism (founder pointed at skills.sh/find-skills); lifecycle placement still open

## Idea In User-Problem Language

Assembly today assembles a *lifecycle* — spec, plan, build, ship — but the agent
walks into every project with the same generic capability. When a project is, say,
a Cloudflare app, the agent should be working with the best Cloudflare-specific
skills, not rediscovering the platform from first principles each session. Ben
wants a step where Assembly **assembles the best skills for the agent to leverage
through the build**, so domain competence travels with the project instead of
living only in whoever happened to prompt well that day.

The name is the thesis: *Assembly* should assemble capabilities, not just phases.

## User And Painful Moment

- Primary user: Ben building real apps with agents across varied stacks
  (Cloudflare, Vercel, etc.).
- Painful moment: starting or returning to a project on a specific platform and
  the agent has no platform-specific skill loaded — it improvises, produces
  generic or subtly-wrong platform code, and the domain knowledge that *does*
  exist publicly (e.g. `cloudflare/skills`) never gets pulled in.
- Desired outcome: when the stack is known, Assembly finds and installs the
  relevant high-quality skills, records them in the project's agents file, and
  every future session leverages them automatically — and Assembly can revisit
  the set as the stack grows.

## Current Workarounds

- The agent improvises platform behavior from training knowledge, with no
  guarantee it is current or idiomatic.
- A human remembers a good skill repo exists and manually installs or pastes it.
- Platform capability arrives ad hoc per environment (e.g. an MCP server wired
  into one session) rather than being a durable, recorded part of the project.

## Narrow Wedge

A thin **capability-assembly step** that composes the existing
[`find-skills`](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)
skill rather than rebuilding a registry:

1. Given the project's stack, run `find-skills` / `npx skills find <stack queries>`
   to discover relevant skills from the skills.sh registry.
2. **Verify before installing.** `find-skills` does not auto-gate search results —
   it instructs the agent never to recommend a skill from search alone, and to
   check install count (prefer 1K+), source-repo reputation, and GitHub stars
   first. The `assemble` skill must perform this verification step before any
   `npx skills add <source>`; this matters most for niche stack queries, where
   search can surface low-reputation skills (including ones shipping scripts/hooks).
   Curation is a step `assemble` runs, not a property inherited for free.
3. Persist the chosen skills into **`AGENTS.md`** — a "Capabilities" section
   listing each assembled skill (name, source, why) — so every future session
   loads them. This is the "update the agents file" piece Assembly owns.
4. Re-runnable: first pass at `init`/scaffold once the stack is known, available
   again whenever the stack grows (new subproject, new platform).

Likely shape: a thin standalone `assemble` skill that `init` calls on scaffold and
the founder can re-invoke later. Assembly composes `find-skills` and owns
persistence; it does not reimplement discovery, ranking, or install.

## How It Composes skills.sh

- `npx skills` is a cross-agent skill package manager (Claude Code, Codex, Cursor,
  etc.); `npx skills find` searches skills.sh, `npx skills add` installs.
- Skills are `SKILL.md` (frontmatter + markdown) discovered in standard dirs;
  publishing is just pushing to a git repo, with install telemetry surfacing it
  on skills.sh.
- This keeps Assembly's standing posture: thin entry skills, don't reinvent,
  preserve the paper trail.

## Lovable Product Moment

Ben says "this is a Cloudflare project" (or Assembly infers it), and from then on
every agent session is already equipped with the best Cloudflare skills — recorded
in `AGENTS.md`, no re-prompting, coherent across sessions and agents. Capability
becomes a durable property of the project, the same way the lifecycle already is.

## Relationship To The 10x Roadmap

This is a **new axis — capability acquisition** — distinct from the four
measurement loops in `.agents/plans/2026-06-01-assembly-10x-roadmap.md` (output
quality, vision alignment, code coherence, autonomous ops). Those loops make the
agent's work *measurably better*; this makes the agent *more domain-capable per
project*. Record it as its own thread so it is not mis-sequenced into the eval
work, and so it does not get dropped.

**Confirmed (2026-06-06):** the two threads stay *separate and cross-linked*, not
merged, and capability assembly was prioritized *ahead of* the measurement stages
— its build is now complete (T1–T4 merged; only a founder-run live smoke remains),
so the measurement axis is next. Both serve the same metric (founder attention per unit of
on-vision product) by the same move — encode once, stop re-doing: the loops
encode taste, this encodes capability. Decision:
`docs/decisions/2026-06-06-two-axes-capability-and-measurement.md`. Coupling seams
to honor later: capabilities ride the same Stage 0 status block; capability
*quality* should eventually be graded by Track B (agent-graded evals) rather than
skills.sh reputation alone; a founder correction about a skill choice belongs in
the Track A ledger; and the discover→verify→filter→install procedure is a
candidate dynamic workflow.

## On Supply-Chain / Trust

Founder's instinct (correct, mostly): this is not the concern it would be for code
dependencies. A skill is instructions the agent reads — closer to fetching docs
than installing a package. The single honest caveat: skills *can* ship scripts/hooks
(Assembly's own skills carry Python and bash), so it is "mostly inert," not "always."
The reputation floor `find-skills` prescribes — install count, source reputation,
GitHub stars, checked *before* install — is a reasonable line, but note it is a step
`assemble` must actively run (see wedge step 2), not an automatic gate the registry
applies for us. No lockfile/vendor/security-auditor apparatus is needed for the
wedge; the verification step is.

## Alternatives Considered

- Rebuild a curated stack→skills registry inside Assembly — rejected as
  reinvention; `find-skills` + skills.sh already do discovery and ranking.
- Auto-discover from GitHub by topic with no registry — higher curation risk, and
  redundant with skills.sh's install-telemetry leaderboard.
- Leave capability to ambient per-environment wiring (e.g. MCP servers) — works in
  one session but is not durable or recorded in the project.

## Adjacency / Seam (out of scope for the wedge)

"Capability" really spans **skills + MCP servers + docs**. Cloudflare reaches a
session as an MCP server + docs-search tool, not a skill bundle. Build the skills
path first via `find-skills`; leave a seam to assemble MCP servers and doc sources
later.

## Main Risks

- Ceremony: an assembly step that adds friction without earning capability.
- Stale `AGENTS.md` capability list drifting from what is actually installed.
- Over-installing low-signal skills; `assemble` must run the `find-skills`
  reputation check (installs, source, stars) before each install, not after.
- Lifecycle placement guessed wrong — over-committing to one trigger before use
  shows where it belongs.

## Open Questions

- Lifecycle placement: `init`-time, a standalone `assemble`, or just-in-time in
  `build`? Founder leans "mostly known at the beginning, revisited over time" —
  so init-seeded + re-runnable, exact surface TBD.
- Stack detection: how does Assembly infer the stack (declared in spec/status vs
  sniffed from the repo)?
- Where the capability list lives: `AGENTS.md` section, the machine-readable
  status block (Stage 0 of the 10x roadmap), or both.

## Recommended Next Step

When ready, `spec` a thin `assemble` skill: inputs (stack/queries), composition of
`find-skills` / `npx skills`, the `AGENTS.md` "Capabilities" section it writes, and
its `init` + standalone re-run triggers. Hold until the founder wants to move from
idea to spec.
