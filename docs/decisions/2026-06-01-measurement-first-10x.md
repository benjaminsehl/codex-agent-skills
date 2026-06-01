# 2026-06-01 Measurement-First 10x Direction

## Status

Accepted

## Context

The founder asked how to take Assembly to 10x its current capabilities across
four axes: output quality, product-vision alignment, code coherence, and
autonomous operations.

Investigation found Assembly is open-loop: skill edits are validated only
structurally, there is no CI, retros accumulate as prose without feeding back
into behavior, and project state lives in prose. The founder is the only sensor
on all four axes — which does not scale and means scaling autonomy first would
scale slop.

Two founder constraints shaped the decision (2026-06-01):

1. Ben has little eval data to draw on.
2. Ben will not personally review code.

## Options Considered

- **Measurement-first** — build eval/alignment/coherence loops, then scale
  autonomy on them.
- **Autonomy-first** — build the post-1.0 orchestrator now, add measurement
  reactively.
- **Output-quality-first** — deepen the existing 1.0 skill loop before any new
  layer.
- **All four in parallel** — concurrent workstreams.

## Decision

Lead with measurement, scope all four loops (see
`docs/plans/2026-06-01-assembly-10x-roadmap.md`), and sequence them so autonomy
only scales as fast as measured quality, alignment, and coherence allow.

The measurement substrate has two tracks because the founder grades direction
and agents grade code:

- **Track A — Course-Correction Ledger.** Sparse, founder-authored, durable
  records of where agent output diverged from intended product direction.
  Machine-readable; a `vision-keeper` reviewer replays them as alignment gates.
  This is the founder's primary interface and the alignment eval at once.
- **Track B — Agent-Graded Quality Evals.** Rubric-based LLM-as-judge plus
  golden fixtures measure code and output quality with no founder in the loop.
  Track A corrections become Track B rubric criteria, so founder taste
  propagates into autonomous grading.

Scope is Ben's personal stack. "Ship 1.0" is not treated as a blocking gate;
the operating rule is to do the most important thing at any moment, and
priorities may change if something more important surfaces.

## Why This Wins

- It instruments exactly the bottleneck — founder attention as sole sensor —
  rather than adding capability on an unmeasured base.
- It fits both founder constraints: sparse founder-authored direction evals
  need little data, and agent-graded code evals need no founder review.
- It makes autonomy safe to scale: the orchestrator inherits objective stop
  conditions (eval regression, alignment violation, coherence drift) instead of
  the founder.
- It compounds: one founder correction raises the floor on every future
  autonomous review.

## Consequences

- Easier: every subsequent skill/persona edit becomes measurable; founder
  attention concentrates on taste.
- Harder: requires building eval infrastructure (runner, rubrics, fixtures,
  CI) Assembly does not have today.
- Riskier: LLM-as-judge can inflate or be gamed — mitigated by anchored
  rubrics, adversarial judging, and occasional founder spot-audits. Eval
  ceremony could itself cost attention — mitigated by keeping the ledger
  founder-authored only on real corrections and fixtures small.
- The post-1.0 orchestrator roadmap is re-grounded: it now depends on the
  measurement loops as prerequisites, not just on the 1.0 control loop.
