# Evals

Assembly's measurement substrate. See
`docs/plans/2026-06-01-assembly-10x-roadmap.md` for the full thesis and
sequencing, and `docs/decisions/2026-06-01-measurement-first-10x.md` for the
direction decision.

Two tracks, because the founder grades direction and agents grade code:

- `course-corrections/` — **Track A.** Sparse, founder-authored records of where
  agent output diverged from intended product direction. The founder's primary
  interface and the alignment eval at once. A `vision-keeper` reviewer replays
  these against new specs, plans, and PRs.
- `rubrics/` — **Track B (planned).** Anchored scoring rubrics an agent judge
  applies to output (specs, code, PRs, transcripts). No founder review in the
  loop.
- `fixtures/` — **Track B (planned).** Golden scenarios a skill or persona edit
  is replayed against so regressions are caught before they reach the founder.

Track A corrections become Track B rubric criteria, so one founder correction
raises the floor on every future autonomous review.

This directory is added to Assembly's own repo first (scope: Ben's personal
stack). Folding `docs/evals/` into the project kernel structure and `init`
scaffold is a roadmap item, not done yet.
