# Assembly

This repo builds the reusable plugin for phase-aware product development. The same plugin bundle at `plugins/assembly/` ships for both Codex (via `.codex-plugin/plugin.json`) and Claude Code (via `.claude-plugin/plugin.json`).

## Start Here

Before choosing work, read:

- `docs/status.md` for the current Assembly project phase, next gate, and active 1.0 questions
- `.agents/AGENT-GUIDANCE.md` for the project copy of the operating protocol
- `docs/product/discovery-1-0.md` for the current product-discovery brief
- `docs/phases/proposal.md` for what 1.0 is meant to prove

Before changing the plugin, inspect:

- `README.md` for user-facing workflow guidance
- `plugins/assembly/docs/SPEC.md` for the plugin contract
- `plugins/assembly/docs/COMMAND_CONTRACT.md` for entry-skill behavior
- `plugins/assembly/references/agent-operating-protocol.md` for phase-aware agent behavior
- `plugins/assembly/scripts/validate_plugin.py` and `plugins/assembly/scripts/validate_skill_graph.py` for validation rules

## Phase-Aware Workflow

When working on this repo, follow the same protocol the plugin teaches:

- Identify whether the change is proposal, prototype, build, or release work.
- Use the relevant skill surface before editing.
- Use `next` when the user asks to continue through the normal process from current project context.
- Use `project-status` first when the phase is unclear, docs need scaffolding, or status needs repair.
- If a user asks to skip prerequisites, warn once, name the missing gate, then proceed if they insist unless a hard safety boundary applies.
- Preserve the paper trail for decisions that future agents will need.

## Editing Rules

- Keep entry skills thin.
- Put detailed guidance in `references/` or `templates/`.
- Keep agent-only project state in `.agents/`; keep product/project reasoning in `docs/`.
- Do not overwrite downstream `AGENTS.md` files in scaffold behavior.
- Keep validators current when adding required files.

## Validation

Run before finalizing changes:

```bash
python3 plugins/assembly/scripts/validate_plugin.py
python3 plugins/assembly/scripts/validate_skill_graph.py
python3 plugins/assembly/scripts/validate_status.py
python3 plugins/assembly/scripts/audit_skill_conflicts.py
python3 -m py_compile plugins/assembly/scripts/*.py
git diff --check
```

CI (`.github/workflows/validate.yml`) runs these on every PR and on `main`.

## Capabilities

Domain skills assembled for Assembly's own stack via the capability-acquisition
behavior (`plugins/assembly/references/capability-acquisition.md`); mirror of the
`capabilities:` list in `docs/status.md`. Assembly is a skills toolkit, not a
platform app, so it has no domain skills to assemble yet.

- _none yet_
