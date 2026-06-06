---
name: init
description: Use to scaffold a new project or subproject workspace. Creates docs/, .agents/, AGENTS.md, and default Claude Code and Codex permission config at the repo root.
---

# Init

## Purpose

Scaffold a project lifecycle workspace at the start of a new project, subproject, or substantial project slice. Runs the deterministic scaffold script, preserves existing files, and hands off to the next phase.

`init` is the canonical scaffold entrypoint. `project-status` covers status, repair, retro, and routing; `init` exists so users do not need to remember scaffold flags.

## References

- `references/project-kernel-structure.md`: structure, paths, and the scaffold contract.
- `references/workflows/project-lifecycle.md`: scaffold mode details and recommended follow-up.
- `references/project-phases.md`: phase gates the scaffold preloads as open questions.
- `references/agent-operating-protocol.md`: missing-prerequisite handling and safety boundaries.

## Workflow

1. State that `init` is active and identify the target repo plus root or subproject scope.
2. Inspect the target root for existing `docs/`, `AGENTS.md`, `.agents/`, `.claude/settings.json`, and `.codex/config.toml` to anticipate what will be created vs preserved.
3. Determine scaffold scope:
   - Root project: omit `--slug` and `--parent`. Files land in `docs/`.
   - Subproject: pass `--slug <slug>` and `--name <name>`. Files land in `.agents/projects/<slug>/`.
   - Nested subproject: also pass `--parent .agents/projects/<parent-slug>`.
4. Run the scaffold script with the chosen flags from the target repo root. Resolve the script path via the plugin runtime: `${CLAUDE_PLUGIN_ROOT}/scripts/scaffold_project.py` (Codex sets the same variable for plugin-hook compatibility). From an Assembly checkout, use `plugins/assembly/scripts/scaffold_project.py` instead.
5. Report the JSON result: `created`, `skipped`, `manual_merge`, `updated`, and `project_dir`.
6. Confirm `.claude/settings.json` and `.codex/config.toml` exist at the repo root so Claude Code and Codex run at max permissions; note the Codex trust requirement when the file is newly created.
7. If `AGENTS.md` was skipped, explain the manual merge using `templates/AGENTS.md`.
8. Recommend the next skill, usually `product-discovery` for a fresh project or `spec` when the proposal is already aligned.

## Verification

- The scaffold ran from the correct root and reports a JSON result.
- Created paths match the requested scope (root or subproject).
- Existing `AGENTS.md`, `.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, `reference/README.md`, `.claude/settings.json`, and `.codex/config.toml` were preserved.
- The response names the next skill and one concrete next action.

## Stop Conditions

- The target root does not exist or is not a directory.
- A subproject scope is requested without `--slug` or with a parent that has no `status.md`.
- The user asks for irreversible cleanup or migration of existing project docs; that is `project-status` repair work, not scaffold.
