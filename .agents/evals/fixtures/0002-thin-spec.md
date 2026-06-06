---
id: 0002-thin-spec
rubric: spec-quality
expect: fail
stub_scores:
  outcome_clarity: 2
  scope_boundaries: 1
  verification: 2
  no_premature_solutioning: 3
---

## Scenario

Same greenfield link-shortener request as fixture 0001, but the `spec` skill produced
a thin, under-scoped spec. This fixture is a deliberate regression: the harness should
conclude `fail`.

## Candidate output

> Build a URL shortener. It takes a URL and makes it shorter. We'll use a database to
> store the mappings and generate random codes. Should be fast and easy to use.

(No stated success criteria, no scope boundary, outcome only gestured at, and it jumps
to implementation — a weak spec that a quality gate should catch.)
