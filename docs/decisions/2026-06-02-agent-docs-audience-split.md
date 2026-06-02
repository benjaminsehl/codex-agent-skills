# 2026-06-02 Split docs/ and .agents/ by audience

## Status

Accepted

## Context

Assembly originally split project files by durability: `docs/` held the durable
project trail (status, phases, product, decisions, tech-design, specs, plans,
prototypes, research, qa, release, projects) and `.agents/` held the agent
operating layer (guidance, log, notes). See
`2026-05-22-root-docs-project-trail.md` and `2026-05-22-agent-only-workspace.md`.

In practice most of `docs/` is written *for the agent* — operational artifacts
it uses to do and resume work — not for a human trying to understand the
product or the code. The founder asked for a cleaner rule: markdown that is for
the agent entirely should live in `.agents/`; documents that benefit a human
and create clarity about how the code works should stay in `docs/`.

## Options Considered

- **Operational vs explanatory (chosen).** `docs/` keeps product, decisions
  (ADRs as human rationale), and tech-design; everything operational —
  status, phases, specs, plans, prototypes, research, qa, release, projects,
  evals — moves to `.agents/`.
- **Aggressive.** `docs/` holds only product and how-the-code-works; even
  decisions move to `.agents/`.
- **Conservative.** Keep the `docs/` trail mostly as-is; move only clearly
  agent-internal artifacts.

## Decision

Split by audience, not durability (founder choice, 2026-06-01):

- **`.agents/`** — everything written for the agent: the operational trail
  (`status.md`, `phases/`, `specs/`, `plans/`, `prototypes/`, `research/`,
  `qa/`, `release/`, `projects/`, `evals/`) plus existing guidance, log, notes.
- **`docs/`** — everything written for a human: `product/`, `decisions/` (the
  human rationale for hard-to-reverse choices), and `tech-design/`.

The two trees nest identically under `projects/<slug>/`, so a subproject's
operational trail is `.agents/projects/<slug>/` and its human docs are
`docs/projects/<slug>/`. This is recursive.

This supersedes the structure portions of `2026-05-22-root-docs-project-trail.md`
and `2026-05-22-agent-only-workspace.md`. Those records are left intact as
historical context; this decision governs going forward.

## Why This Wins

- A human opening `docs/` sees only what helps them understand the product and
  code — no operational noise.
- The agent's working state is consolidated in one place (`.agents/`), which is
  also where an external operator (e.g. Hermes) reads project state.
- The audience rule is easier to apply than "is this durable?" — the test is
  "who is this written for?"
- It scales recursively to subprojects without special cases.

## Consequences

- Easier: human onboarding to a repo; locating the agent trail; reasoning about
  what an operator reads.
- Harder/migration cost: `status.md` moved to `.agents/status.md`, so the
  session-start hook, `validate_status.py`, the scaffold, the kernel-structure
  reference, all skills, and the operating protocol were updated. CI and the
  scaffold smoke test assert the new layout.
- Historical decision records and `.agents/log.md` keep their original path
  references as accurate history; only active guidance was updated.
- Scaffolded projects now get both trees; `scaffold_project.py` writes
  operational files to `.agents/` and human docs to `docs/`.
