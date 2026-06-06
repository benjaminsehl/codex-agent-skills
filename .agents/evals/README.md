# Evals

Assembly's measurement substrate. See
`.agents/plans/2026-06-01-assembly-10x-roadmap.md` for the full thesis and
sequencing, and `docs/decisions/2026-06-01-measurement-first-10x.md` for the
direction decision.

Two tracks, because the founder grades direction and agents grade code:

- `course-corrections/` — **Track A.** Sparse, founder-authored records of where
  agent output diverged from intended product direction. The founder's primary
  interface and the alignment eval at once. A `vision-keeper` reviewer replays
  these against new specs, plans, and PRs.
- `rubrics/` — **Track B.** Anchored scoring rubrics an agent judge applies to
  output (specs, code, PRs, transcripts). No founder review in the loop. Skeleton
  shipped (`spec-quality.md` starter); the full per-skill set is Stage 2.
- `fixtures/` — **Track B.** Golden scenarios a skill or persona edit is replayed
  against so regressions are caught before they reach the founder. Skeleton shipped
  (a passing + a regression fixture).

Track A corrections become Track B rubric criteria, so one founder correction
raises the floor on every future autonomous review.

## Runner (Stage 0 skeleton)

`plugins/assembly/scripts/eval_runner.py` grades a fixture against its rubric:
weight-aggregate per-criterion scores, compare to the rubric threshold, emit a
verdict, exit non-zero on a regression. Spec: `.agents/specs/eval-harness.md`.

```bash
python3 plugins/assembly/scripts/eval_runner.py --selftest        # all fixtures, CI-gated
python3 plugins/assembly/scripts/eval_runner.py --fixture <path>  # grade one
```

The judge is pluggable: this slice ships a deterministic `stub` backend (it exercises
the harness path reproducibly); the real LLM-as-judge backend lands in Stage 2 behind
the same interface (`--judge llm`).

This directory is added to Assembly's own repo first (scope: Ben's personal
stack). Folding `.agents/evals/` into the project kernel structure and `init`
scaffold is a roadmap item, not done yet.
