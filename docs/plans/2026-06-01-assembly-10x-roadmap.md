# Roadmap: Assembly 10x

Last updated: 2026-06-01
Status: direction accepted (founder, 2026-06-01); slices not yet planned
Scope: Ben's personal stack (not broad adoption, not multi-project — yet)

## Thesis: Assembly is open-loop; 10x is closing four loops

Assembly today is an unusually thoughtful prompt-and-skill library with strong
process discipline. But mechanically it has **no feedback loops and no
measurement**:

- Skill edits are validated only structurally (`validate_plugin.py`,
  `validate_skill_graph.py`) — nothing measures whether a change makes agent
  *output* better or worse.
- There is no CI; the validators run only when an agent remembers to.
- Retros and decisions accumulate as prose but nothing feeds them back into
  `next`/`project-status`. The system gathers documents, not capability.
- Project state lives in prose, so every consumer re-derives it.

The deep consequence: **the founder is currently the only sensor on all four
target axes** — output quality, product-vision alignment, code coherence, and
the autonomy boundary are all measured by Ben looking at the work. That is
exactly the thing that does not scale, and it is why scaling autonomy on
today's base would mostly scale slop.

**10x = replace founder-as-sole-sensor with four instrumented loops, sequenced
so autonomy only scales as fast as measured quality, alignment, and coherence
allow.** Founder attention then concentrates on product taste — the one input
that genuinely does not scale — and everything else self-measures.

## The measurement substrate (the lead)

Founder decision (2026-06-01): lead with measurement, but shaped to two
constraints — Ben has little eval data to draw on, and Ben will not personally
review code. So the substrate has two tracks: the founder grades *direction*,
agents grade *code*.

### Track A — Course-Correction Ledger (founder-authored, sparse, product)

The founder's primary interface. Every time the agent's output diverges from
where Ben wanted product direction to go, that divergence is captured **once**
as a durable, structured entry: the situation, what the agent did, what Ben
wanted instead, and the generalizable principle behind the correction.

- Low volume is the point. Even 5–20 entries is a high-signal taste corpus.
- Entries are machine-readable (frontmatter + body) so an agent can replay them.
- A `vision-keeper` reviewer loads the ledger and checks every new spec, plan,
  and PR against the accumulated corrections: "does this repeat a correction Ben
  already made? does it trip an anti-goal?" The ledger is the alignment loop and
  the alignment eval at once.
- Lives at `docs/evals/course-corrections/` (see that directory's README for the
  entry template).

This is how Ben's taste gets encoded once and stops being re-litigated. It is
the cheapest possible eval system: the founder authors a case only when he is
already course-correcting — never manufactured ceremony.

### Track B — Agent-Graded Quality Evals (autonomous, code & output)

Because Ben will not review code, code and output quality must be measured by
agents, not the founder.

- **Rubric-based LLM-as-judge.** Reviewer personas score output (specs, code,
  PRs, transcripts) against explicit rubrics with concrete anchors, producing a
  graded score plus rationale.
- **Golden fixture scenarios** for skill regression: a small seed set
  (greenfield init, messy retrofit, stale-status repair, ambiguous `next`,
  missing-product-gate `build`) that a skill or persona edit is replayed
  against; the judge scores the transcript against a rubric.
- **Gating:** a skill/persona edit that regresses a rubric or trips a ledger
  case blocks (in CI, once Stage 0 lands).

**Track A feeds Track B.** Founder course-corrections become rubric criteria the
agent-judge enforces, so Ben's sparse direction corrections propagate into the
autonomous code grading. That coupling is the multiplier: one founder correction
raises the floor on every future autonomous review.

## The four loops

Scoped here in full (per founder request); sequenced measurement-first below.

| Axis (founder's words) | Loop | Mechanism |
| --- | --- | --- |
| Output quality | Eval harness | Track B fixtures + rubrics + runner, gated in CI |
| Product-vision alignment | Course-correction loop | Track A ledger + `vision-keeper` reviewer gating specs/PRs |
| Code coherence | Coherence loop | Decision/architecture index + `coherence-reviewer` + build-verification gates (lint/type/format/characterization) + read-only desloppification pass |
| Autonomous operations | Operator-ready protocol | Operators such as Hermes, OpenClaw, or a manual harness session consume Assembly's protocol, autonomy profile, and stop conditions |

### Connective tissue (small, unblocks all four)

- **Machine-readable status block** — ship a small YAML block that exposes phase,
  next gate, autonomy profile, verification contract, and escalation rules so
  tools, CI, and external operators read state instead of re-parsing prose.
- **CI** — run the validators (and later the evals) on every PR. Coherence of
  Assembly itself should not rest on an agent remembering four python scripts.
- **Lessons index + a per-cycle `compound` step** — turn retros into a
  structured index `next` and `project-status` actually consult, so the system
  gets measurably better from use instead of merely accumulating prose. Borrow
  the discipline from Every's compound-engineering loop (see
  `docs/research/2026-06-02-compound-engineering-and-dynamic-workflows.md`):
  capture learnings after *every* slice, not just at end-of-project retro. A
  thin `compound` step writes any new founder correction to the ledger and any
  reusable pattern to the lessons index. (Borrow the mechanism, not the 37-skill
  surface — that cuts against "few entrypoints, deep references.")
- **Portable protocol primer** — package the Assembly operating protocol (today
  split across root `AGENTS.md` and `references/agent-operating-protocol.md`) as
  one canonical, runtime-agnostic primer any agent can load: a plugin-based
  runtime (Codex/Claude Code skills) or a bare CLI agent you hand the doc to.
  The lifecycle skills become thin pointers to it. This keeps behavior
  consistent across heterogeneous agents and external operators. Hermes,
  OpenClaw, or a similar always-on system can consume the primer, choose the
  execution harness, and escalate through its own interface (for example
  iMessage) without Assembly becoming runtime-specific. Keep it thin (orient →
  phase → gates → leave evidence → escalation) pointing to deep references, per
  "few entrypoints, deep references."

## Sequencing

Measurement-first. Each stage leaves evidence the next stage depends on.

### Stage 0 — Foundation (do first; cheap, unblocks everything)

- Machine-readable status block in `docs/status.md`.
- CI workflow running the four validators on every PR.
- Eval harness skeleton: a runner, the rubric file format, and 1–2 fixtures.

Exit evidence: a PR shows CI green on the validators; one fixture scores through
the runner end to end.

### Stage 1 — Alignment loop (founder's primary interface)

- `docs/evals/course-corrections/` ledger live, with the entry template.
- `vision-keeper` persona that loads the ledger + north-star + anti-goals and
  gates specs, plans, and PRs against them; fans into `review` and `ship`.
- Backfill the ledger from existing decisions where a founder correction is
  already on record.
- Ledger ingestion can be automated as a **dynamic workflow** (see the research
  note): mine recent sessions and review comments for recurring corrections,
  cluster them with parallel agents, adversarially verify each candidate ("would
  this rule have prevented a real mistake?"), and distill survivors into ledger
  entries. The iMessage/founder loop seeds the ledger; this workflow mines it.

Exit evidence: one spec or PR is checked against the ledger and the
`vision-keeper` either passes it or names which correction/anti-goal it trips.

### Stage 2 — Output-quality loop

- Rubrics for the existing public skills (what does a good `spec`, `plan`,
  `build` slice, `review` look like — anchored, not vibes).
- Expand the fixture set to cover each lifecycle skill.
- Wire eval gating into CI: a skill/persona edit runs its fixtures and must not
  regress its rubric.
- The eval runner is a natural **dynamic workflow**: a worktree agent per
  fixture run plus a *separate* grader agent per rubric (a distinct judge is what
  defeats self-preferential bias), with a skeptic agent to limit false positives.
  Ship it as a workflow inside the eval skill (JS in the skill folder, referenced
  from `SKILL.md` as a template). See the research note.

Exit evidence: a deliberate skill regression is caught by the eval gate in CI.

### Stage 3 — Code-coherence loop

- Architecture/decision index a `coherence-reviewer` enforces (Chesterton's
  fence on record): new code is checked against existing patterns and prior
  decisions.
- Move lint/type/format/characterization gates from prose recommendations in
  `build` into executed verification.
- Read-only desloppification pass (Stage 5 of the original post-1.0 roadmap):
  drift findings on a branch with a PR, never silent rewrites.

Exit evidence: the coherence-reviewer flags one real duplication or
decision-reversal in a fixture; build verification fails on an injected
type/lint error.

### Stage 4 — Autonomous operations (operator-ready protocol)

- Assembly does not own a single orchestrator. It owns the portable protocol,
  autonomy profile, evidence packet, and stop-condition contract that an operator
  can consume.
- External operators such as Hermes, OpenClaw, or a future harness runner use the
  same protocol to choose work, launch Codex/Claude/Pi/OpenCode sessions or other
  executors, report progress, and escalate through their own human interface.
- Objective stop conditions come from loops 1–3: eval regression,
  ledger/anti-goal violation, coherence drift, failed verification, or an
  approval boundary. That is what lets a low-oversight project run many PRs deep
  between founder check-ins without making Assembly runtime-specific.
- **Dynamic workflows are the in-session scale substrate, complementary to the
  operator.** The operator (Hermes) decides *what* runs and escalates to the
  founder; a dynamic workflow executes the *scaled* step (large sweeps,
  migrations, fan-out review) through a codified, rerunnable script. Its "no
  mid-run user input — run each stage as its own workflow for sign-off"
  constraint matches the founder-gate model exactly. See the research note and
  `references/orchestration-patterns.md`.

Exit evidence: an operator or simulated operator runs a bounded slice end to end
from the portable protocol primer and halts on a seeded eval regression rather
than on a founder check-in.

## The 10x metric for this effort

**Founder attention per unit of shipped, on-vision product.** 10x means Ben
makes the same quality of product with ~10x less direction-correcting attention,
because corrections are captured once and enforced autonomously thereafter.

Honest leading indicators:

- The rate of *novel* course-corrections per project slice trends down over time
  (the ledger should show diminishing new entries as the system internalizes
  taste — not because Ben stopped looking, but because the same mistake stops
  recurring).
- Agent-graded quality scores trend up across skill edits, with no founder code
  review in the loop.
- CI catches skill regressions before they reach Ben.

## Risks and anti-goals

Carried from Assembly's existing principles, applied to this effort:

- **Eval ceremony replacing product work.** The ledger is founder-authored only
  when Ben is already course-correcting; fixtures and rubrics stay small and
  high-signal. If maintaining the harness costs more attention than it saves,
  that is a regression against the 10x metric itself.
- **LLM-as-judge gaming / grade inflation.** Mitigate with concretely anchored
  rubrics, an adversarial judge posture, and occasional founder spot-audits of
  the judge — the one place the founder deliberately touches a code eval.
- **Over-fitting to the fixture set.** Keep fixtures representative; rotate them
  as real projects surface new situations.
- **Autonomy outrunning measurement.** The sequencing is the mitigation:
  Stage 4 depends on Stages 1–3 producing trustworthy stop conditions.

## Out of scope (this roadmap)

- Broad adoption / generalization for other builders (founder: Ben's personal
  stack).
- Multi-project / portfolio orchestration (per-project loop only, as before).
- Treating "ship 1.0" as a blocking gate — founder: always do the most
  important thing now; priorities can change if something more important
  surfaces.

## First next step

Use `plan` to break Stage 0 (status block + CI + eval-harness skeleton) into
verifiable slices, then `build` the first slice.
