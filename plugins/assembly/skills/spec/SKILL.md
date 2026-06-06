---
name: spec
description: Use when defining a project, feature, or significant change before implementation; turns intent into a reviewed specification.
---

# Spec

## Purpose

Define what should be built before coding starts. Surface user pain, clarify success criteria, and save a spec future planning and build can trust. The founder owns every product decision; the agent surfaces options and gathers evidence.

## References

- `references/workflows/engineering-delivery.md`: spec mode and acceptance criteria.
- `references/product-discovery-checklist.md`: discovery framing — user, pain, wedge.
- `references/project-phases.md`: proposal-to-build phase gate.

## Workflow

1. State that the `spec` workflow is active and summarize the user goal in one or two sentences.
2. Read existing project docs, commands, and prior specs when a repo already exists.
3. Run mini-discovery before drafting: ask at most 4 questions per round (one or two rounds is fine) framed around user, pain, and wedge. Always fire — even when the spec is being repaired or invoked via routing from `build`. Use the explicit options-list pattern when surfacing alternatives.
4. Decide signal density:
   - Fresh discovery exists in `docs/discovery/` or a recent spec → lightweight spec (objective, success criteria, scope, open questions).
   - Thin or stale signals → full spec (objective, users, pain, wedge, stack, commands, structure, style, testing, boundaries, success criteria, open questions).
5. Surface assumptions and explicit non-goals before treating the spec as final.
6. Save the spec as `SPEC.md`, `docs/SPEC.md`, or `.agents/projects/<slice>/spec.md`, following the target repo's conventions.
7. Stop at a founder review gate. Do not auto-continue into planning.

## Verification

- The spec file exists.
- Mini-discovery questions and founder answers are captured in the spec.
- Assumptions, non-goals, and open questions are visible.
- Success criteria are specific enough to test.
- Boundaries include always, ask first, and never categories.
- Signal density (lightweight vs full) is named with reasoning.

## Stop Conditions

- Success cannot be defined from the current information after mini-discovery.
- Major assumptions would be risky to make without founder review.
- The request conflicts with repository or safety boundaries.
- Mini-discovery surfaces a product gap too large for inline questions — route to `product-discovery` instead.
