---
id: spec-quality
area: spec
version: 1
criteria:
  - id: outcome_clarity
    weight: 2
    description: States the user-facing outcome and what good looks like.
  - id: scope_boundaries
    weight: 2
    description: Names what is explicitly out of scope.
  - id: verification
    weight: 1
    description: Defines how the result will be checked.
  - id: no_premature_solutioning
    weight: 1
    description: Stays at the behavior level; does not prescribe implementation prematurely.
threshold: 3.5
---

# Rubric: Spec Quality

Track B starter rubric for grading the output of the `spec` skill. Each criterion is
scored 1–5 against the anchors below. The runner takes a weighted mean and compares
it to `threshold` (3.5).

This is an *illustrative* starter, not a binding product judgment — Stage 2 refines
the rubric set, and Track A course-corrections seed real criteria.

## Anchors

### outcome_clarity (weight 2)

- **5** — The user-facing outcome and an explicit "what good looks like" are both
  stated in observable terms.
- **3** — Outcome is present but vague, or "good" is implied rather than stated.
- **1** — No clear outcome; reads as a task list with no destination.

### scope_boundaries (weight 2)

- **5** — Explicitly names what is out of scope, with reasoning where non-obvious.
- **3** — Some boundary stated, but leaves obvious ambiguities open.
- **1** — No scope boundary; the spec could expand indefinitely.

### verification (weight 1)

- **5** — Concrete, checkable success criteria a reviewer can apply.
- **3** — Verification gestured at but not concretely checkable.
- **1** — No notion of how the result is verified.

### no_premature_solutioning (weight 1)

- **5** — Stays at the behavior/outcome level; implementation choices deferred.
- **3** — Mixes some implementation detail into the behavior spec.
- **1** — Largely an implementation plan masquerading as a spec.
