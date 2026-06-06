# 2026-06-06 Split docs/ and .agents/ by audience

## Status

Accepted

## Context

Assembly originally split project files by durability: `docs/` held the durable
project trail (status, phases, product, decisions, tech-design, specs, plans,
prototypes, research, qa, release, projects) and `.agents/` held the agent
operating layer (guidance, log, notes). See
`2026-05-22-root-docs-project-trail.md` and `2026-05-22-agent-only-workspace.md`.

In practice most of `docs/` is written *for the agent* — operational artifacts
it uses to do and resume work — not for a human trying to understand the product
or the code. The founder asked for a cleaner rule: markdown that is for the agent
entirely lives in `.agents/`; documents that benefit a human and create clarity
about how the code works stay in `docs/`. The boundary was confirmed as
operational vs explanatory.

(An earlier attempt at this migration was prepared but could not merge cleanly
because the parallel capability-assembly workstream advanced `main` on the old
`docs/` structure. This decision re-applies the split on current `main`,
absorbing the capability-assembly files.)

## Options Considered

- **Operational vs explanatory (chosen).** `docs/` keeps product, decisions
  (ADRs as human rationale), and tech-design; everything operational moves to
  `.agents/`.
- **Aggressive.** `docs/` holds only product and how-the-code-works; even
  decisions move to `.agents/`.
- **Conservative.** Move only clearly agent-internal artifacts.

## Decision

Split by audience, not durability:

- **`.agents/`** — everything written for the agent: the operational trail
  (`status.md`, `phases/`, `specs/`, `plans/`, `prototypes/`, `research/`,
  `qa/`, `release/`, `projects/`, `evals/`) plus existing guidance, log, notes.
- **`docs/`** — everything written for a human: `product/`, `decisions/` (the
  human rationale for hard-to-reverse choices), and `tech-design/`.

The two trees nest identically under `projects/<slug>/`. Recursive.

This supersedes the structure portions of `2026-05-22-root-docs-project-trail.md`
and `2026-05-22-agent-only-workspace.md`, which are left intact as historical
context.

## Why This Wins

- A human opening `docs/` sees only what helps them understand the product and
  code — no operational noise.
- The agent's working state is consolidated in `.agents/`, which is also where an
  external operator (e.g. Hermes) reads project state.
- "Who is this written for?" is an easier test than "is this durable?"
- It scales recursively to subprojects without special cases.

## Consequences

- `status.md` moved to `.agents/status.md`, so the session-start hook,
  `validate_status.py`, the scaffold, the kernel-structure reference, all skills,
  the operating protocol, and `detect_stack.py`'s docstring were updated. CI and
  the scaffold smoke test assert the new layout.
- The capability-assembly spec moved to `.agents/specs/capability-assembly.md`;
  its discovery brief stays in `docs/product/`. The `capabilities:` validation in
  `validate_status.py` is preserved.
- Historical decision records and `.agents/log.md` keep their original path
  references as accurate history; only active guidance was updated.
- `tasks/` (a separate top-level agent task dir) is left in place for now; folding
  it into `.agents/` is a possible follow-up.
- Scaffolded projects now get both trees.
