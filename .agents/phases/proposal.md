# Proposal Phase

## What Becomes 10x Better

A user can return to any substantial project, say `next`, and the agent will know the phase, missing context, correct skill, and next useful action from the local project trail.

## What Good Looks Like

Assembly 1.0 feels like a reliable human-led project operating system for agents: lightweight enough to use daily, structured enough to prevent skipped thinking, and proven on real projects.

## Desired Outcomes

- `next` works as the default continuation phrase in fresh agent sessions.
- Project scaffolding creates a useful root `docs/` trail without overwriting existing instructions.
- `project-status` can diagnose phase, missing prerequisites, and recovery plan from real repo artifacts.
- Product, engineering, QA, and business lenses are available without overwhelming the active skill surface.
- Material GitHub-backed work ends in a descriptive PR that explains why, first principles, and approach; the agent decides draft vs ready and promotes to ready autonomously once reviewer sub-agents are satisfied and verification is green; it merges and deploys autonomously when `pre-live`, escalating only product/UX decisions and (when `live`) the merge-to-default-branch gate.
- Installation, migration, validation, and troubleshooting docs are accurate enough for a cold user.
- 1.0 is proven against Assembly itself and CFO, with Hyper as a stretch retrofit proof.

## Assumptions

- The primary user will tolerate a small amount of project documentation if it makes agents materially better.
- A compact skill surface with references is easier for agents to use than many overlapping triggerable skills.
- Natural-language invocation is good enough; slash commands are not required for 1.0.
- The strongest near-term value is personal reliability, not broad marketplace polish.

## Principles

- Optimize for agent usefulness in service of human founder judgment.
- Keep workflow gates useful, not ceremonial.
- Preserve Chesterton's fence: record why decisions exist before future agents change them.
- Make skipped prerequisites visible instead of blocking all momentum.
- Prefer a few durable entry skills over many clever skills.

## Risks

- The workflow could become too heavy and slow down building.
- `next` could feel magical but brittle if project status is stale or ambiguous.
- GitHub handoff could become noisy if agents create PRs for tiny changes or include unrelated files.
- Plugin installation and session refresh behavior may remain rough.
- Public users may have skill conflicts or different project conventions.
- 1.0 could overfit Ben's current workflow before enough real project use.

## Decision Gate

Proposal is ready to leave this phase when the user accepts the 1.0 wedge, proof projects, release blockers, and non-goals.
