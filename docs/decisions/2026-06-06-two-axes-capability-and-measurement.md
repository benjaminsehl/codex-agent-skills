# 2026-06-06 Two axes: capability assembly and the measurement loops

## Status

Accepted

## Context

Two threads are live at once and were evolving in parallel:

- **The measurement-first 10x roadmap**
  (`.agents/plans/2026-06-01-assembly-10x-roadmap.md`) — close four feedback
  loops (output quality, vision alignment, code coherence, autonomous ops) so
  autonomy scales only as fast as measured quality. See
  `2026-06-01-measurement-first-10x.md`.
- **Capability assembly** (`.agents/specs/capability-assembly.md`,
  `docs/product/discovery-capability-assembly.md`) — a shared
  capability-acquisition behavior that assembles the best domain skills for a
  project's stack and records them durably. Currently the active build gate
  (T1/T2 merged; T3 next).

They share one metric — *founder attention per unit of on-vision product* — and
one move: **encode something once so it stops being re-done each session.** The
measurement loops encode *taste/quality* (stop re-correcting); capability
assembly encodes *domain competence* (stop re-equipping).

Two things needed a decision: how the threads relate in the docs, and whether
capability assembly shipping ahead of the measurement work is intended or drift.
The 10x roadmap was silent on capability assembly, so the active build read as
off-roadmap drift to anyone reading the strategic plan.

## Options Considered

- **One roadmap, two tracks** — fold capability assembly into the 10x roadmap as
  a named parallel track and reframe the thesis around "encode taste *and*
  capability."
- **Keep separate, cross-link (chosen)** — the 10x roadmap stays the measurement
  program; capability assembly stays its own axis; add explicit cross-references
  and a recorded priority so neither reads as drift.
- **Capability as a co-equal pillar** — restructure the strategic framing around
  two named pillars rather than four loops plus a side track.

## Decision

1. **Two separate axes, cross-linked — not merged.** Capability acquisition makes
   the agent *more domain-capable per project*; the measurement loops make its
   work *measurably better*. Distinct mechanisms, distinct planning docs. This
   preserves the original intent (discovery brief) that capability assembly not be
   mis-sequenced behind the eval build.
2. **Priority: finish capability assembly first.** Complete T3 (call-site wiring)
   and T4 (boundaries/smoke), then resume the measurement program at Stage 0's
   eval-harness skeleton. This is a deliberate "most important thing now" call,
   explicitly permitted by the 10x roadmap's own out-of-scope clause — not drift.
   (As of this record, that is satisfied: T3 (#20) and T4 (#23) are merged, so the
   capability build is complete bar a founder-run live smoke, and measurement
   Stage 0 is now the next dev work.)
3. **Record the coupling seams** so they are not lost while the threads stay
   separate (revisit when the relevant loop exists):
   - *Data layer (already shared):* assembled capabilities ride the same
     `assembly-status/v1` block Stage 0 shipped.
   - *Capability quality is currently unmeasured:* capability assembly trusts
     skills.sh reputation (installs/stars) as a proxy. Whether an assembled skill
     actually improves output for *this* project is a Track B (agent-graded eval)
     question. When Track B exists, capability quality should flow through it
     rather than reputation alone.
   - *Shared correction logic:* the course-correction ledger's test ("would this
     rule have prevented a real mistake?") is the same logic as capability
     assembly's reputation-and-fit verification; a founder correction about a skill
     choice belongs in the ledger.
   - *Execution shape:* capability assembly is a candidate dynamic workflow
     (generate-and-filter + adversarial verification), per
     `.agents/research/2026-06-02-compound-engineering-and-dynamic-workflows.md`.

## Why This Wins

- Keeps capability assembly from being mis-sequenced behind the eval build — the
  original, still-valid concern.
- Keeps the measurement roadmap focused rather than diluted.
- Makes both the *separation* and the *priority* explicit, so the active build no
  longer reads as drift against a measurement-first plan.
- Preserves the integration seams without paying integration cost now.

## Consequences

- Cross-reference notes added to the 10x roadmap (a "related axis and current
  priority" note), the capability discovery brief (confirmed decision + seams),
  and `.agents/status.md` (the active gate is intentional, ahead of measurement
  Stage 0).
- No change to the active build sequence: capability T3 → T4, then measurement
  Stage 0.
- Revisit the "capability quality is unmeasured" seam when Track B lands; until
  then, reputation-gated install is the accepted line (see the discovery brief's
  trust analysis).
