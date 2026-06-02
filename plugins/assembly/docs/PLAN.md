# Implementation Plan: Assembly Plugin

> **Historical record.** This plan documents the original Codex-first build with completed checkpoints; Codex-specific phrasing below reflects the state at the time of each task. The bundle has since gained a Claude Code manifest (`.claude-plugin/plugin.json`) and marketplace catalog so the same skills, references, and scripts work in both runtimes. See [SOURCE_NOTES.md](SOURCE_NOTES.md) and [INSTALL.md](INSTALL.md) for the current adaptation.

## Overview

Build the plugin in careful layers: first lock the command contract, then add validation, then add the engineering entry skills, then vendor or adapt the underlying skills, then add the product/business/design layer and run smoke tests in a throwaway project. The command layer is load-bearing, so every phase should leave us with a reviewable artifact and a clear verification checkpoint.

## Architecture Decisions

- The command-like workflows are Codex skills, not slash commands. Codex plugin manifests expose `skills`, and the local spec does not define a `.codex/commands` equivalent.
- Entry skills stay thin. They orchestrate and route, while detailed workflows live in deeper skills.
- The plugin should be self-contained. Depending on `/Users/sai/.agents/skills` would make it fragile across machines and Codex sessions.
- Validation is part of the product. A broken skill graph is a product bug, not a documentation typo.
- `ship` needs a Codex-specific adaptation because Claude's command assumes automatic parallel subagents, while Codex should only spawn subagents when explicitly authorized.

## Phase 1: Contract and Scaffold

### Task 1: Finalize Plugin Manifest

Description: Make `.codex-plugin/plugin.json` valid and intentional for a public developer-tools plugin.

Acceptance criteria:

- [x] Manifest parses as JSON.
- [x] `skills` points to `./skills/`.
- [x] No placeholder paths reference missing hooks, MCP servers, apps, screenshots, or icons.

Verification:

- [x] `python3 -m json.tool .codex-plugin/plugin.json >/dev/null`

Files likely touched:

- `.codex-plugin/plugin.json`

Estimated scope: XS

### Task 2: Lock the Initial Entry-Skill Contract

Description: Create `docs/COMMAND_CONTRACT.md` defining each initial entry skill's trigger, inputs, required outputs, underlying skills, and refusal or stop conditions.

Acceptance criteria:

- [x] All initial entry skills have explicit responsibilities.
- [x] Each entry skill has success evidence.
- [x] The contract names what the entry skill must not do.

Verification:

- [x] Manual review against `docs/SPEC.md`.

Files likely touched:

- `docs/COMMAND_CONTRACT.md`

Estimated scope: S

### Checkpoint: Foundation

- [x] Spec reviewed.
- [x] Plan reviewed.
- [x] Manifest valid.
- [x] Command contract approved.

## Phase 2: Validation Harness

### Task 3: Add Plugin Shape Validator

Description: Add a script that verifies the plugin manifest, required directories, and skill file anatomy.

Acceptance criteria:

- [x] Fails when `plugin.json` is invalid.
- [x] Fails when a required entry skill is missing.
- [x] Fails when a `SKILL.md` lacks required frontmatter.

Verification:

- [x] `python3 scripts/validate_plugin.py`

Files likely touched:

- `scripts/validate_plugin.py`
- `tasks/todo.md`

Estimated scope: M

### Task 4: Add Skill Graph Validator

Description: Add a validator for the entry-skill mapping and underlying skill references.

Acceptance criteria:

- [x] Fails if an entry skill omits a required underlying skill.
- [x] Fails if an entry skill references a missing skill directory.
- [x] Flags entry skills that exceed a conservative size limit.

Verification:

- [x] `python3 scripts/validate_skill_graph.py`

Files likely touched:

- `scripts/validate_skill_graph.py`
- `docs/COMMAND_CONTRACT.md`

Estimated scope: M

### Checkpoint: Guardrails

- [x] Manifest validation passes.
- [x] Skill graph validation passes after implementation and failed before required skills existed.
- [x] We know validation will catch drift before skills become operational.

## Phase 3: Entry Skills

### Task 5: Implement `spec` and `plan`

Description: Add the first two entry skills for defining and planning work.

Acceptance criteria:

- [x] `skills/spec/SKILL.md` routes to definition skills and saves a spec.
- [x] `skills/plan/SKILL.md` routes to planning and task breakdown.
- [x] Both include clear human-review gates.

Verification:

- [x] `python3 scripts/validate_plugin.py`
- [x] `python3 scripts/validate_skill_graph.py`
- [x] Manual smoke prompt documented in `docs/SMOKE_TESTS.md`.

Files likely touched:

- `skills/spec/SKILL.md`
- `skills/plan/SKILL.md`
- `tasks/todo.md`

Estimated scope: M

### Task 6: Implement `build` and `test`

Description: Add implementation and verification entry skills.

Acceptance criteria:

- [x] `build` chooses one pending task and requires test/build evidence.
- [x] `test` supports feature TDD and bug Prove-It workflows.
- [x] Browser verification is called out for UI/runtime work.

Verification:

- [x] Validators pass.
- [x] Manual smoke prompt documented in `docs/SMOKE_TESTS.md`.

Files likely touched:

- `skills/build/SKILL.md`
- `skills/test/SKILL.md`
- `tasks/todo.md`

Estimated scope: M

### Task 7: Implement `review`, `code-simplify`, and `ship`

Description: Add quality, simplification, and launch decision entry skills.

Acceptance criteria:

- [x] `review` leads with file/line findings when code is available.
- [x] `code-simplify` preserves behavior and verifies after each meaningful simplification.
- [x] `ship` produces GO/NO-GO with blockers, risks, and rollback plan.
- [x] `ship` is Codex-safe about subagents and parallelization.

Verification:

- [x] Validators pass.
- [x] Manual smoke prompt documented in `docs/SMOKE_TESTS.md`.

Files likely touched:

- `skills/review/SKILL.md`
- `skills/code-simplify/SKILL.md`
- `skills/ship/SKILL.md`
- `tasks/todo.md`

Estimated scope: M

### Checkpoint: Initial Entry Surface

- [x] All initial entry skills exist.
- [x] All initial entry skills pass graph validation.
- [x] Entry skills remain thin.

## Phase 4: Underlying Skill Library

### Task 8: Vendor or Adapt Required Skills

Description: Bring in the deeper skill library needed by the entry points.

Acceptance criteria:

- [x] Required underlying skill directories exist.
- [x] Source attribution is preserved.
- [x] Any local Codex-specific changes are documented.

Verification:

- [x] Validators pass.
- [x] Diff review confirms expected vendored files are present.

Files likely touched:

- `skills/*/SKILL.md`
- `references/*`
- `docs/SOURCE_NOTES.md`

Estimated scope: L; split if needed

### Task 9: Add Reference Checklists and Persona Adaptation

Description: Add the supporting checklists and decide how reviewer personas should be represented in Codex.

Acceptance criteria:

- [x] Security, performance, accessibility, and testing references are available.
- [x] Persona behavior needed by `ship` is available as skills or documented subagent prompts.
- [x] Codex subagent limitations are represented accurately.

Verification:

- [x] Validators pass.
- [x] Manual `ship` smoke expectation includes all required audit dimensions.

Files likely touched:

- `references/*`
- `skills/*`
- `docs/COMMAND_CONTRACT.md`

Estimated scope: M

### Checkpoint: Self-Contained Plugin

- [x] The plugin no longer depends on global `/Users/sai/.agents/skills`.
- [x] All entry-skill references resolve locally.
- [x] Validation passes from the plugin root.

## Phase 5: Smoke Testing and Installation

### Task 10: Create Throwaway Smoke Fixtures

Description: Add tiny fixture scenarios for each entry skill so we can test behavior without risking real projects.

Acceptance criteria:

- [x] Fixture instructions exist for spec, plan, build, test, review, simplify, and ship.
- [x] Smoke tests document expected evidence.

Verification:

- [x] Manual smoke run checklist documented for execution after install.

Files likely touched:

- `docs/SMOKE_TESTS.md`
- `fixtures/*`

Estimated scope: M

### Task 11: Decide Local Installation Path

Description: Decide whether to add this plugin to `~/.agents/plugins/marketplace.json` or keep it as a manually referenced local plugin.

Acceptance criteria:

- [x] Installation path is documented.
- [x] No local `~/.agents/plugins/marketplace.json` entry is added without explicit approval.

Verification:

- [x] Manual install or discovery check.

Files likely touched:

- `docs/INSTALL.md`
- Maybe `~/.agents/plugins/marketplace.json` only with explicit approval

Estimated scope: S

### Final Checkpoint

- [x] Validators pass.
- [x] Smoke checklist is documented for real project verification.
- [x] The entry skills are ready for real project use.
- [x] Remaining open questions are documented.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Entry skills become bloated duplicates | High | Enforce size limit and graph validator |
| Codex invocation differs from Claude slash commands | High | Make entry skill names simple and document prompt examples |
| `ship` assumes unauthorized subagent fan-out | High | Codex-specific `ship` contract with explicit authorization rules |
| Upstream content drifts | Medium | Record source commit and add source notes |
| Validation gives false confidence | Medium | Pair scripts with manual smoke tests |
| Plugin depends on this machine's global skills | High | Vendor/adapt required skills into plugin |

## Follow-Up Layer

- [x] Added product-discovery, founder-review, business-model-review, design-plan-review, qa, health-check, retro, and learn.
- [x] Added founder-product-critique, business-model-evaluation, and live-qa-methodology support skills.
- [x] Added product, business, design, and QA references.
- [x] Extended validators and smoke docs for the full entry-skill set.
- [x] Added public MIT license metadata.

## Personal Project Stack Layer

- [x] Added `new-project` to scaffold a project workspace and proposal gate.
- [x] Added `prototype` to create throwaway tangible artifacts before production build.
- [x] Added `project-status` to answer current phase, missing artifacts, next gate, and next skills.
- [x] Added `scripts/scaffold_project.py` for deterministic `docs/` and `.agents/projects/<slug>/` scaffolds.
- [x] Added project phase, project kernel, Matt Pocock skills, and Hyper retrofit references.
- [x] Extended validators, command contract, install docs, smoke tests, source notes, and manifest metadata.
- [x] Clarified recursive projects, root `docs/` as the project workspace, child project scaffolds, and Chesterton's fence paper-trail expectations.
- [x] Simplified the scaffold convention from `docs/project/` to root `docs/` and updated the README into a user guide.
- [x] Added phase-aware AGENTS guidance, downstream template, canonical operating protocol, scaffold support, and validator coverage.
- [x] Added `introspect` as the deeper workflow audit and status-repair skill behind `project-status`.
- [x] Shrunk the public skill surface to 11 lifecycle skills and moved support workflows behind references.
- [x] Added install conflict guidance and advisory local skill conflict audit.
- [x] Added `next` as a narrow contextual continuation entry skill that dispatches only from evidence-backed project state.

## Decisions

- This is public and MIT licensed.
- The first build copied workflow skills from local installed skills and copied support material from upstream commit `f17c6e88c904dc747381c374312c2d58e10647ae`.
- Entry skills use short names only for the first version.
- Matt Pocock's `skills` and `agent-kernel` are cited as inspiration only; this layer is an original Codex-native project lifecycle adaptation.
- Version `0.7.0` makes a pre-install breaking cleanup: lifecycle skills stay public, support workflows move to references, and existing user-skill conflicts are documented as a migration concern.
- Version `0.7.1` adds `next` because the one-word continuation command is itself a useful product interface, while keeping the heavy status and lifecycle logic in references.
