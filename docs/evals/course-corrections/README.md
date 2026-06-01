# Course-Correction Ledger

Track A of Assembly's measurement substrate. The founder's primary interface for
encoding product taste **once** so the same misalignment stops recurring.

## When to add an entry

Add an entry whenever the agent's output diverged from where the founder wanted
product direction to go — and only then. This ledger is authored on real
corrections, never manufactured. Low volume is the point: even 5–20 high-signal
entries is a strong taste corpus.

Capture the *generalizable* correction, not just the one-off fix. The goal is a
principle a future agent (and the `vision-keeper` reviewer) can replay against
new specs, plans, and PRs.

## How it is used

A `vision-keeper` reviewer (planned, Stage 1) loads this ledger plus the
north-star and anti-goals, and checks new work against it: "does this repeat a
correction already on record? does it trip an anti-goal?" Each entry's
`principle` also becomes candidate criteria for Track B rubrics, so founder
corrections propagate into autonomous code grading.

## Entry format

One file per correction: `NNNN-short-slug.md`, zero-padded sequential id.

```markdown
---
id: 0001
date: YYYY-MM-DD
area: <skill / phase / surface this applies to, e.g. spec, next, product-discovery>
severity: principle | strong | nudge
tags: [scope, copy, naming, ...]
---

# <short title of the correction>

## Situation

What context was the agent working in (project, phase, prompt)?

## What the agent did

The output or direction the agent took.

## What the founder wanted instead

Where product direction should have gone, in user-facing terms.

## Principle

The generalizable rule a future agent should apply. This is the part the
`vision-keeper` replays and Track B rubrics borrow.

## Alignment check

A concrete test a reviewer can apply to new work to detect a repeat
("flag any spec that ... ").
```

## Backfill

Existing decision records may already contain founder corrections worth
promoting into this ledger. Backfilling those is a Stage 1 task in the roadmap.
