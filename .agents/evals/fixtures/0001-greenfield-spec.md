---
id: 0001-greenfield-spec
rubric: spec-quality
expect: pass
stub_scores:
  outcome_clarity: 5
  scope_boundaries: 4
  verification: 4
  no_premature_solutioning: 4
---

## Scenario

Greenfield project, proposal phase. The founder asked: "spec a link-shortener: paste
a long URL, get back a short one that redirects." The `spec` skill was invoked to
produce a behavior spec.

## Candidate output

> **Objective.** A visitor pastes a long URL and receives a short link that, when
> visited, redirects to the original. Good looks like: a valid URL returns a short
> code in under a second, and visiting the short link 302-redirects to the original.
>
> **Out of scope.** Custom vanity codes, analytics, account systems, link expiry —
> none ship in this slice; the wedge is paste → short link → redirect.
>
> **Verification.** Paste a known URL, confirm a short code is returned; visit the
> code, confirm a 302 to the original; paste an invalid string, confirm a clear
> rejection.
>
> **Behavior, not implementation.** Storage engine, code-generation scheme, and
> hosting are deferred to tech-design; this spec fixes only observable behavior.
