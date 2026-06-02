# Product Discovery: Assembly 1.0

Last updated: 2026-05-27

## Idea In User-Problem Language

Ben wants to stay in product language the whole time while agents execute the entire product-building lifecycle. The deeper magic is not a single moment of orientation; it is being able to speak in product terms and aims while quality stays extremely high, vision coherence stays high across multiple sessions and multiple agents, and the human stays in product-direction work instead of translating between product intent and engineering implementation.

## User And Painful Moment

- Primary user: Ben building real apps and project slices with agents.
- Built in public; other builders may adopt it but are not the audience 1.0 is designed around.
- Painful moment is a cluster:
  - Returning to a repo and the agent has no idea where things are.
  - Starting a fuzzy idea and the agent produces work before clarifying direction.
  - Agents asking too many low-value questions, or asking in engineering-implementation language when product-implication framing would be clearer.
  - Agents asking the wrong questions — missing the product/user/viability lens entirely.
  - Agents doing work before checking product direction, then producing output that has to be thrown away.
- Desired outcome: agents orient themselves, name the phase, identify missing prerequisites in product-implication terms, select the right workflow, ask only the questions that matter, and proceed only when the next action is evidence-backed.

## Current Workarounds

- Ad hoc prompts like "continue" or "what should we do?"
- Loose skills installed globally with overlapping names.
- Repo-local markdown notes that are helpful but not consistently structured.
- Manual reminders to check product vision, principles, decisions, QA, and release gates.
- Manual reminders to commit, push, open descriptive draft PRs, explain why the work matters, self-review, simplify, and mark PRs ready.
- Built-in platform plugins that help with execution but do not own the product lifecycle.

## Narrow 1.0 Wedge

Install Assembly, scaffold a repo, and stay in product language. The agent should:

- read the local project trail,
- identify proposal, prototype, build, or release phase,
- clarify what is being built, why it matters, and what good looks like when the project trail does not already answer those questions,
- ask only high-leverage questions, in product-implication language (never engineering detail),
- name missing prerequisites,
- choose the right public skill,
- delegate to specialized subagents when the work calls for it,
- update status when project-doc edits are in scope,
- for material GitHub-backed changes, `build` commits and pushes the topic branch; `ship` opens the descriptive draft PR (asking founder for draft vs ready), runs self-review and simplification, and always asks before promoting to ready, merging, or deploying — honoring the always-ask floor on top,
- preserve enough evidence and decision context that the next session and the next agent stay coherent with the project vision.

Two everyday surfaces of the wedge:

- `next` on returning to a project, with the agent orienting itself from the trail and either proceeding cleanly or asking the one product question that matters.
- Continuous product-language conversation: Ben describes intent and aims; agents handle discovery, spec, plan, build, test, QA, review, and release without forcing Ben to translate into engineering.

## Recommended 1.0 Stance

Assembly 1.0 should optimize for "Ben's personal stack that works beautifully" first. It is built in public; other builders may adopt it, but they are not the audience 1.0 is designed around.

That means:

- Personal reliability beats broad marketplace polish.
- Public usability still matters enough to keep installation, migration, conflict audits, privacy notes, and docs clean.
- The same plugin bundle ships and behaves in both Codex and Claude Code; broader runtime portability is not a near-term goal.
- The post-1.0 orchestrator should stay visible as the next horizon, but 1.0 should prove the agent control loop first: status, phase, next action, gates, GitHub handoff, and recovery — with product-language conversation and vision coherence across sessions as the headline magic.

## Recommended Proof Path

- Required: Assembly self-hosts its own workflow and proves `next` can guide this repo from proposal to release.
- Required: CFO proves the greenfield/restart project setup because it is a good moment to install the project trail cleanly.
- Stretch: Hyper proves retrofit behavior against a messy, high-context real app without forcing risky migration all at once.

## Post-1.0 North Star

A post-1.0 orchestrator becomes the in-project general manager that can coordinate scoped agent sessions through Assembly.

The intended split:

- The orchestrator owns the project roadmap, prioritization, scheduling, and continuity within one project.
- Assembly owns the project protocol: status, phases, gates, docs, and handoff rules.
- Agent runtimes (Codex, Claude Code, etc.) own focused implementation sessions inside clean branches or worktrees.

The smallest useful future proof is not "support every agent runtime." It is: the orchestrator can inspect an Assembly project, choose the next scoped task, launch or instruct an agent runtime to execute it, and require a PR-based handoff. Cross-project orchestration is an open question for after 1.0; the per-project loop is the only required scope.

## Lovable Product Moment

Ben stays in product language across a whole project. He describes intent and aims; agents handle discovery, spec, plan, build, test, QA, review, and release at high quality through effective skills, careful context engineering, and correctly delegated specialist subagents. Vision coherence stays high across sessions and across agents — the next agent picks up where the last one left off, from evidence in the project trail, not from guesswork.

A daily expression of this: returning after days away, saying `next`, and the agent telling Ben what phase the project is in, why, what is missing, and either performing the next safe action or asking the one product question that matters.

## Alternatives

- Addy-style individual skills: useful patterns, but not a cohesive project operating system.
- GStack-style sprint roles: useful product/company methodology, but too broad and runtime-specific for this pass.
- Built-in runtime plugins: strong execution tools, but not a lifecycle owner.
- Manual `AGENTS.md` instructions: helpful, but too passive without status and phase artifacts.
- Broader runtime portability beyond Codex and Claude Code: plausible someday, but not important enough to compete with finishing the dual-runtime plugin and proving post-1.0 orchestration.

## Founder Critique

Verdict: narrow, then prove.

Assembly should name the long-term ambition (product-language conversation, vision coherence across sessions and agents, post-1.0 orchestrator) without pretending 1.0 delivers it. The 1.0 release proves the human-led agent control loop that the rest needs: project trail, phase awareness, clarifying questions in product-implication terms, next-step routing, gates, and PR handoff. Post-1.0 orchestration comes after that loop is trustworthy.

## Business Model Lens

Near-term business model is not the main constraint. Assembly should be evaluated as leverage for Ben to build better products faster.

Potential future value (post-1.0, all optional):

- A public open-source workflow that becomes a personal brand asset.
- A premium orchestrator layer, hosted project dashboard, or team workflow only after the local plugin proves real value.
- Consulting or product-building acceleration if the workflow produces visibly better apps.

Riskiest viability assumption for the open-source surface: other builders will only adopt a project-doc workflow if the daily `next` and product-language conversation experience is immediately and repeatedly useful. This is a constraint on quality, not a 1.0 audience target.

## Main Risks

- Too much ceremony: agents write documents instead of improving the product.
- Too little structure: `next` becomes a polite guess.
- Install/session refresh friction hides the value.
- Skill conflicts make behavior unpredictable.
- Agents may finish with local diffs instead of reviewable GitHub artifacts.
- Agents drift away from product-implication language and start asking in engineering terms.
- Vision coherence breaks across sessions: a later agent contradicts an earlier decision because the trail is incomplete.
- The stack overfits Ben's current projects before being tested on enough project types.

## Evidence Needed Before 1.0

- Fresh install and upgrade works from `benjaminsehl/assembly` in both Codex and Claude Code. Current evidence: `codex plugin marketplace upgrade assembly` confirmed the local marketplace install was current at `0.8.3` after PR #2; Claude Code install/upgrade still needs a fresh smoke pass.
- Fresh agent session sees `assembly:next` in both runtimes. Current evidence: `assembly:next` is available from the installed `0.8.3` Codex bundle; this should be rechecked for the 1.0 release candidate in both runtimes.
- Assembly itself uses root `docs/` and status successfully. Current evidence: `.agents/status.md` now records post-merge status and next-gate routing.
- Scaffolded projects separate durable docs, agent-only `.agents/` context, and raw `reference/` material.
- At least one real external project, ideally Hyper or CFO, gets a useful Assembly retrofit.
- `next` behaves well in at least proposal, build, and release-like states.
- Agents ask in product-implication language, not engineering detail, when product direction is missing.
- Vision coherence holds across at least one multi-session, multi-agent slice: the second session does not contradict the first.
- At least one end-to-end change is committed, pushed, opened as a descriptive draft PR, self-reviewed, simplified, and marked ready.
- Docs explain how to migrate from loose skills and how to handle conflicts.

## Candidate 1.0 Release Criteria

- Public plugin installs as `assembly` and exposes only the candidate public skill surface (currently 13 skills), with any drift recorded.
- `project-status` can scaffold and repair a project trail without overwriting existing `AGENTS.md`.
- Scaffolds keep `AGENTS.md` at the root, agent-only context in `.agents/`, durable project reasoning in `docs/`, and raw source material in `reference/`.
- `next` is reliable enough to be the default continuation command.
- GitHub-backed work has a reliable PR handoff loop: `build` commits and pushes; `ship` opens the descriptive draft PR and always asks before promoting to ready, merging, or deploying. The always-ask floor is honored on top, regardless of product-gate clarity.
- Validators cover manifest, marketplace layout, skill graph, references, and conflict audit.
- README gives a clear user guide from install to first project to ongoing use.
- 1.0 has a release checklist, smoke-test evidence, and a short retro from real project use.
- The docs explicitly state that 1.0 ships as a dual-runtime plugin for Codex and Claude Code, and post-1.0 orchestration is the next strategic horizon.

## Recommended Next Step

Write a 1.0 spec for the dual-runtime plugin (Codex and Claude Code), with post-1.0 orchestration captured as the next strategic horizon rather than a 1.0 dependency.
