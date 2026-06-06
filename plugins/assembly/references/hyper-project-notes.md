# Hyper Project Notes

Use this when retrofitting a project that already has many useful notes but did not start from the four-phase project structure.

The inspected Hyper checkout showed valuable artifacts spread across:

- Top-level product and design docs.
- `.agents/` kernel-style notes, logs, knowledge files, and decisions.
- Raw source material that should become `reference/` instead of project docs.
- `.agents/plans/` dated specs and implementation plans.
- API docs and migration plans.

This is useful context, but it creates a resume problem: a future session can find many documents without a single current phase, next gate, or project verdict.

## Retrofit Approach

1. Use `project-status` first. Do not move files before understanding which project slice is being assessed.
2. Create phase docs in the root docs tree:
   - Whole app: `/Users/sai/hyper/docs/`.
   - App slice: `/Users/sai/hyper/.agents/projects/<slug>/`.
   - Nested feature: `/Users/sai/hyper/.agents/projects/<parent>/projects/<slug>/`.
3. Link existing artifacts instead of copying them:
   - Product/design docs into proposal.
   - Existing specs and dated plans into build.
   - QA evidence and release decisions into release.
   - `.agents/decisions` or ADRs into `docs/decisions/`.
   - Raw Ladder-style imports, screenshots, transcripts, and vendor materials into `reference/`.
4. Fill gaps with explicit "missing" entries, especially:
   - What becomes 10x better.
   - What good looks like.
   - Assumptions and principles.
   - Prototype verdict, if no prototype phase existed.
   - Release grading and follow-up learning.
5. Keep `.agents/` for agent-only operating context if the repo already uses it. Promote durable product, technical, or decision context into `docs/`; keep raw source material in `reference/`.

## Retrofit Output

For each slice, produce:

- Current phase.
- Existing artifacts linked by path.
- Missing proposal/prototype/build/release evidence.
- Next recommended skills.
- One next action.
