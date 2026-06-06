---
name: product-discovery
description: Product strategy gateway. Use for raw ideas, user pain, founder critique, business-model pressure tests, and pre-spec product direction.
---

# Product Discovery

## Purpose

Turn a raw idea or fuzzy direction into a sharper product opportunity before writing a build spec. Focus on user pain, narrow wedge, evidence, ambition, and business viability.

Default to interviewing the user as founder/product director. Do not make product calls for the user unless they explicitly ask you to decide, ask you to recommend a direction, or the project docs already contain enough evidence to support a recommendation.

Flag business, user, and viability concerns; do not decide them. The founder is the only person who can make those calls.

## References

- `references/product-discovery-checklist.md`: discovery output shape.
- `references/business-model-checklist.md`: ICP, pricing, distribution, retention, and cost risk.
- `references/design-quality-checklist.md`: UX/taste lens for planned user-facing flows.
- `references/workflows/product-strategy.md`: interview, ideation, founder critique, business review, and design-plan modes.

## Workflow

1. State that `product-discovery` is active and summarize the idea in user-problem language.
2. Identify whether the user wants interview mode or delegated mode:
   - Interview mode is the default for raw ideas, fuzzy direction, or short prompts.
   - Delegated mode applies only when the user asks you to make the calls, recommend a direction, or continue from strong existing project evidence.
3. In interview mode, adapt question shape to idea maturity. All questions must be in product-implication language (user, value, risk, viability) rather than engineering-implementation detail:
   - Well-formed idea (clear user + pain + rough wedge): ask 1-3 sharpening questions on the highest-leverage gaps.
   - Raw idea (idea exists but pain/wedge/distribution are fuzzy): ask in themed batches of 2-4 related questions, waiting between batches. Themes: user + pain, wedge + scope, distribution + viability, success + risks.
   - Fuzzy idea (solution looking for a problem, or no concrete user named): ask one high-leverage question at a time and wait for each answer before continuing.
4. Interview coverage must include user, painful moment, current workaround, urgency, desired outcome, wedge, constraints, distribution, success evidence, risks, and recommended next skill before producing a discovery brief.
5. Before recommending a wedge, scope, or success criteria, make sure the conversation or project trail answers what is being built, why it matters, what good looks like, the risks and non-goals, and rollback or hold criteria (when the change will touch production behavior).
6. In delegated mode, state the assumptions you are making, mark recommendations as recommendations, and name which assumptions need later validation. Never silently decide business, user, or viability questions; flag them explicitly even in delegated mode.
7. Generate and compare narrow wedges, alternatives, risks, and evidence paths only after the key user/product inputs are clear enough.
8. Apply founder critique when ambition, differentiation, scope, or product delight is the named risk (risk-triggered, not by default).
9. Apply the business-model lens when ICP, pricing, distribution, retention, or cost structure matters. Surface concerns and trade-offs; do not pick a pricing, ICP, or distribution strategy for the founder.
10. Apply the design-plan lens when the next step is a planned UI or user flow.
11. Produce a discovery brief covering user, pain, wedge, alternatives, risks, evidence needed, open questions, and recommended next skill.
12. Save the brief to `docs/product/discovery-<slug>.md` in the active project or subproject, using a slug derived from the idea name. Update `.agents/status.md` to point to it. Append a one-line entry to `.agents/log.md` naming the brief and the recommended next skill.
13. Stop before `spec` unless the user asks to continue.

## Verification

- User pain is concrete and tied to a moment or workflow.
- Key product choices came from the user or were clearly labeled as delegated assumptions.
- What is being built, why it matters, what good looks like, risks, and rollback are explicit or named as open questions.
- The recommended wedge is narrow enough to build and learn from.
- Alternatives and current workarounds are named.
- Business, user, and viability concerns are flagged, not decided.
- Open questions are visible instead of hidden behind confident recommendations.
- The discovery brief is saved to `docs/product/discovery-<slug>.md` and referenced from `.agents/status.md`.
- The next evidence step is explicit.

## Stop Conditions

- The user, pain, or urgency cannot be stated concretely.
- The idea is still a solution looking for a problem.
- Product direction depends on user values, appetite, or taste and the user has not delegated that decision.
- The next step would be implementation before discovery evidence or user assumptions are clear.
