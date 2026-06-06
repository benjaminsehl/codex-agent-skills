# Spec: Eval-Harness Skeleton (Stage 0, Track B)

Last updated: 2026-06-06
Status: accepted (engineering, pre-live autonomy); skeleton slice of Stage 0
Roadmap: `.agents/plans/2026-06-01-assembly-10x-roadmap.md` (Stage 0 → Stage 2)
Direction: `docs/decisions/2026-06-01-measurement-first-10x.md`

## Objective

Ship the smallest honest Track B primitive: a **runner**, a **rubric format**, and
**1–2 fixtures**, such that *one fixture scores through the runner end to end* (the
roadmap's Stage 0 exit evidence). This is the foundation the Stage 2 output-quality
loop builds on — not the full loop.

## What this is and is not

- **Is:** the harness plumbing — parse a rubric, parse a fixture, produce
  per-criterion scores, weight-aggregate, compare to a threshold, emit a structured
  verdict, exit non-zero on a regression. Plus the file formats and a deterministic
  self-test that runs in CI.
- **Is not:** the real LLM-as-judge (Stage 2), the full per-skill rubric set
  (Stage 2), `vision-keeper` / Track A wiring (Stage 1), or CI gating that blocks a
  skill edit on a rubric regression (Stage 2). The seams for those are left clean.

## Design

### Judge is pluggable; the skeleton ships a deterministic stub

The judge is fundamentally an LLM-as-judge, which is non-deterministic and needs an
API key — neither belongs in a Stage 0 CI selftest. So the runner separates
**plumbing** from **judgment**:

- `build_judge_prompt(rubric, fixture)` assembles the exact prompt a real judge
  receives (rubric criteria + anchors + candidate output). This artifact is real and
  is asserted by the selftest.
- A `--judge` backend produces per-criterion scores:
  - `stub` (default, CI): returns the fixture's declared `stub_scores`. It judges
    nothing — it exercises the *aggregation + threshold + verdict + exit-code* path
    deterministically, so "a fixture scores end to end" is true and reproducible.
  - `llm` (Stage 2): scores the candidate live against the anchors. Not wired in this
    slice; selecting it fails with a clear "lands in Stage 2" message rather than
    half-acting.

The runner contract (load → build prompt → score → aggregate → verdict) is identical
across backends, so Stage 2 slots the real judge in behind a stable interface.

### Rubric format (`.agents/evals/rubrics/<id>.md`)

YAML frontmatter carries the machine-readable scoring schema; the markdown body
carries the human-readable anchors a judge reads.

```yaml
---
id: spec-quality
area: spec                 # which skill/surface this grades
version: 1
criteria:                  # each scored 1-5 by the judge
  - id: outcome_clarity
    weight: 2
    description: States the user-facing outcome and what good looks like.
  # ...
threshold: 3.5             # weighted mean on the 1-5 scale; >= passes
---
```

### Fixture format (`.agents/evals/fixtures/<nnnn>-<slug>.md`)

A golden scenario: the context a skill was given plus a candidate output to grade,
and the expected verdict so the harness is self-checking.

```yaml
---
id: 0001-greenfield-spec
rubric: spec-quality
expect: pass               # pass | fail — what the runner should conclude
stub_scores:               # plumbing only: scores the stub backend returns
  outcome_clarity: 5
  # ...
---
## Scenario
...
## Candidate output
...
```

### Runner CLI (`plugins/assembly/scripts/eval_runner.py`)

- `--fixture <path> [--judge stub|llm]` — grade one fixture; print per-criterion
  scores, weighted aggregate, threshold, and verdict; exit 0 on pass, 1 on
  regression.
- `--selftest` — run every fixture under `.agents/evals/fixtures/` with the stub
  backend and assert each verdict matches its `expect`; also assert
  `build_judge_prompt` includes every criterion. Exit 0/1. Mirrors
  `detect_stack.py --selftest`.
- Stdlib + PyYAML, matching `validate_status.py`: if PyYAML is absent (bare local
  `python3`), `--selftest` prints SKIP and exits 0; CI installs it.

## Files

- `plugins/assembly/scripts/eval_runner.py` (new)
- `.agents/evals/rubrics/spec-quality.md` (new — starter rubric)
- `.agents/evals/fixtures/0001-greenfield-spec.md` (new — passing)
- `.agents/evals/fixtures/0002-thin-spec.md` (new — regression)
- `.agents/evals/README.md` (rubrics/fixtures now exist; document the runner)
- `plugins/assembly/scripts/README.md` (document `eval_runner.py`)
- `.github/workflows/validate.yml` (add the selftest step)

## Out of scope (this slice)

- The real LLM judge backend (Stage 2).
- A rubric per lifecycle skill (Stage 2); `spec-quality` is one illustrative starter.
- Track A `vision-keeper` and ledger backfill (Stage 1).
- Gating a skill edit on a rubric regression in CI (Stage 2).
- Folding `.agents/evals/` into the `init` scaffold (later roadmap item).

## Success criteria

- `eval_runner.py --selftest` passes locally (with PyYAML) and in CI.
- The passing fixture yields a pass verdict and exit 0; the regression fixture yields
  a fail verdict and exit 1, via the same code path.
- The rubric and fixture formats are documented and parseable.
- `--judge llm` fails with a clear Stage-2 message; no other backend half-acts.

## Notes on taste

The `spec-quality` criteria are an *illustrative* starting rubric, not a binding
product judgment. Stage 2 refines the rubric set, and Track A course-corrections seed
real criteria — so a founder correction raises the floor on every future review.
