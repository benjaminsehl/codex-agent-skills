# Capability Acquisition (shared behavior)

The single procedure for equipping a project with the best domain skills for its
stack (e.g. `cloudflare/skills` for a Cloudflare project), so per-domain competence
travels with the project instead of living in whoever prompted well. Spec:
`docs/specs/capability-assembly.md`.

This is a **shared behavior, not a skill**. Three call sites invoke it; the public
skill surface does not grow:

- **`init`** — after scaffold, when a stack is detectable, run this (stack-scoped).
- **`build`** — just-in-time, when a slice touches platform behavior the agent has
  no loaded skill for: run this with a **task-scoped** query (e.g. "Cloudflare
  Durable Objects alarms"), not a broad stack guess — as an explicit boundary
  clause, then proceed with the acquired skill.
- **`project-status`** — an explicit "re-assemble capabilities" route when the
  stack grows (new subproject, new platform).

Assembly composes skills.sh (`find-skills` / `npx skills`); the work owned here is
stack detection, the verification gate, and durable persistence.

## Procedure

1. **Detect.** Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/detect_stack.py --root <repo>`
   (from an Assembly checkout: `plugins/assembly/scripts/detect_stack.py`). It
   returns JSON `{root, stacks, signals}`. For a `build` trigger, the query is the
   concrete task, not the whole stack.
2. **Confirm.** Present the inferred stack(s) and the signals that matched; wait for
   founder confirmation or correction before searching. Never search or install on
   an unconfirmed guess. Seed signals: `references/stack-signals.md`.
3. **Discover.** Run `npx skills find <queries>` derived from the confirmed
   stack/task against the skills.sh registry.
4. **Verify before installing.** Apply the `find-skills` reputation gate to every
   candidate — install count (prefer ~1K+), source-repo reputation, GitHub stars
   (treat <100-star repos with skepticism) — **before** any install. Never install
   from search results alone.
5. **Install verified.** Auto-install only matches that clear the bar, via
   `npx skills add <source>`. List below-bar / niche matches as optional candidates
   the founder can opt into; never auto-install them.
6. **Report.** For each install, report name, source, reputation signals, and why.
   Flag any installed skill that ships executable scripts/hooks (not just
   instructions).
7. **Persist (both surfaces).** Reconcile the result into the project trail (see
   below).
8. **Log.** Append a one-line entry to `.agents/log.md` naming what was assembled.

If `npx skills` (Node) is unavailable, stop with a clear message naming the missing
dependency rather than half-acting. Works identically in Codex and Claude Code.

## Persistence

Capability is recorded in two places so humans and tooling/orchestrator both read
it. Reconcile, never duplicate; preserve founder-authored entries.

### `AGENTS.md` "Capabilities" section (always)

One entry per assembled skill. Re-running updates in place; it does not append
duplicates and does not drop entries a human added by hand.

```markdown
## Capabilities

Domain skills assembled for this project's stack via the capability-acquisition
behavior. Mirror of the status block's `capabilities:` list where that block exists.

- `cloudflare-skills` — source: `cloudflare/skills` — Workers/Wrangler domain skill (12k installs)
```

### Status block `capabilities:` list (when the block exists)

When the project's `docs/status.md` carries the machine-readable
`assembly-status/v1` block (Assembly's own repo does; fresh scaffolds do not yet),
mirror each entry into a `capabilities:` list:

```yaml
capabilities:
  - name: cloudflare-skills
    source: cloudflare/skills
    why: Workers/Wrangler domain skill
    installs: 12000
```

If the block is absent, persist the `AGENTS.md` section only and note that the
machine-readable mirror is unavailable — do not invent a block.

## Boundaries

**Always:** run the reputation gate before any install; report every install with
source + reputation; preserve founder-authored Capabilities entries when
reconciling.

**Ask first:** anything on the always-ask floor (credentials, external messaging,
irreversible/destructive ops); installing a skill that ships executable
scripts/hooks when it is below the reputation bar.

**Never:** install from search results without verification; auto-install below-bar
or niche matches; overwrite or drop a founder-authored Capabilities entry.
