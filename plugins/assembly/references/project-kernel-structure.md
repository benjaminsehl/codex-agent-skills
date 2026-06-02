# Project Structure

This is a project-focused adaptation of the agent-kernel idea: small, inspectable markdown files that let a future agent restart with less drift. It is not a long-running-agent memory system.

## Contents

- The audience split
- Root project
- Agent operational trail
- Human documentation
- Subprojects
- What belongs where
- Scaffold command

Projects are recursive. A whole repo can be a project, and an agent layer, native client, release, or feature inside it can also be a project with its own proposal, prototype, build, and release trail.

## The Audience Split

Markdown is split by **who it is written for**, not by how durable it is:

- **`.agents/`** holds everything written for the agent: the operational trail it uses to do and resume work — status, phases, specs, plans, prototypes, research, QA, release, and child-project trails — plus agent guidance, log, and notes. A human may read it, but it is not written for a human.
- **`docs/`** holds everything written for a human: documents that create clarity about the product and how the code works — product vision and principles, decisions (the human rationale), and tech design.

The two trees nest identically: a subproject lives under `projects/<slug>/` in both. Chesterton's fence still applies: future work should find the original reasoning before changing or removing a structure.

## Root Project

Use this shape for the main project in a repo:

```text
AGENTS.md
.claude/
`-- settings.json
.codex/
`-- config.toml
.agents/                      # agent operational trail
|-- AGENT-GUIDANCE.md
|-- log.md
|-- notes/
|   `-- README.md
|-- status.md
|-- phases/
|   |-- proposal.md
|   |-- prototype.md
|   |-- build.md
|   `-- release.md
|-- specs/
|   `-- README.md
|-- plans/
|   `-- README.md
|-- prototypes/
|   `-- README.md
|-- research/
|   `-- README.md
|-- qa/
|   `-- README.md
|-- release/
|   `-- README.md
`-- projects/
    `-- README.md
docs/                         # human documentation
|-- README.md
|-- product/
|   |-- vision.md
|   `-- principles.md
|-- decisions/
|   `-- README.md
`-- tech-design/
    `-- README.md
reference/
`-- README.md
```

## Agent Operational Trail

Keep `AGENTS.md` at the repo root so agents have an obvious entrypoint. Put all agent operational material under `.agents/`.

Instruction-like project files use uppercase names, such as `.agents/AGENT-GUIDANCE.md`. Records and working context use lowercase names, such as `.agents/log.md`, `.agents/notes/`, and `.agents/status.md`.

Do not put the operational trail in `docs/`. `docs/` is human documentation; `.agents/` is the agent operating layer and the project trail.

## Human Documentation

`docs/` is written to help a person understand the product and the code: what is being built and why (`product/`), the reasoning behind hard-to-reverse choices (`decisions/`), and how the system is designed (`tech-design/`). If a document exists only so the agent can do or resume work, it belongs in `.agents/`, not here.

## Subprojects

A subproject splits the same way, under `projects/<slug>/` in both trees:

```text
.agents/projects/<project-slug>/   # operational trail: status, phases, specs, ...
docs/projects/<project-slug>/      # human docs: README, product, decisions, tech-design
```

Nested subproject:

```text
.agents/projects/<parent-slug>/projects/<child-slug>/
docs/projects/<parent-slug>/projects/<child-slug>/
```

Prefer a single root pair of trees over package-level docs. Only use a different root when the work is genuinely in a different repo or the user explicitly chooses that boundary.

## What Belongs Where

- `AGENTS.md`: top-level entrypoint for agent behavior in the repo.
- `.claude/settings.json`: Claude Code project settings. The scaffold sets `permissions.defaultMode` to `bypassPermissions` so Claude Code runs at maximum permissions without approval prompts.
- `.codex/config.toml`: Codex project settings. The scaffold sets `approval_policy = "never"` and `sandbox_mode = "danger-full-access"` so Codex runs at maximum permissions; Codex applies these only to projects you have trusted.
- `reference/`: raw source material, imports, screenshots, transcripts, datasets, vendor docs, and evidence that should stay close to the project.

Agent operational trail (`.agents/`):

- `.agents/AGENT-GUIDANCE.md`: project-visible copy of the phase-aware agent operating protocol.
- `.agents/log.md`: append-only agent handoff events, skipped gates, recovery notes, and project-operation changes.
- `.agents/notes/`: temporary agent working notes and open loops.
- `.agents/status.md`: current phase, evidence, next gate, next skills, and one next action.
- `.agents/phases/proposal.md`: outcomes, assumptions, principles, risks, existing constraints, and what good looks like.
- `.agents/phases/prototype.md`: prototype question, artifacts, findings, and verdict.
- `.agents/phases/build.md`: approved direction, slices, acceptance criteria, verification, and risks.
- `.agents/phases/release.md`: QA, polish, ship decision, grading, and follow-up work.
- `.agents/specs/`: approved behavior specs.
- `.agents/plans/`: implementation plans and task breakdowns.
- `.agents/prototypes/`: prototype notes, links, verdicts, and cleanup status.
- `.agents/research/`: observed evidence, source notes, and market or user research.
- `.agents/qa/`: tested flows, bugs, repro steps, evidence, and regression recommendations.
- `.agents/release/`: launch, rollback, ship, and post-release notes.
- `.agents/projects/`: operational trail of child projects that need their own phase trail.

Human documentation (`docs/`):

- `docs/product/`: vision, user, painful moment, promise, principles, non-goals.
- `docs/decisions/`: decision records only for trade-offs that are hard to reverse, surprising, and consequential.
- `docs/tech-design/`: architecture, interfaces, data model, runtime constraints, security, performance, migrations.
- `docs/projects/`: human documentation of child projects.

## Scaffold Command

Root project:

```bash
python3 scripts/scaffold_project.py --root /path/to/repo --name "Project Name"
```

This creates `AGENTS.md` only when it does not already exist. Existing project instructions must be merged manually.

The scaffold also creates `.agents/AGENT-GUIDANCE.md`, `.agents/log.md`, `.agents/notes/README.md`, and `reference/README.md` when absent, and writes both the `.agents/` operational trail and the `docs/` human documentation.

It also creates `.claude/settings.json` and `.codex/config.toml` when absent, granting Claude Code and Codex maximum permissions so neither runtime prompts for approval. Both are preserved when they already exist so the scaffold never clobbers existing permission config; the scaffold reports a manual-merge note telling you which keys to set. Codex applies `.codex/config.toml` only to projects you have trusted.

`.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, and `reference/README.md` are protected once they exist so child-project force scaffolds cannot overwrite repo-level agent instructions, notes guidance, or reference guidance. `.agents/log.md` is append-only; scaffold runs append a new entry instead of rewriting prior handoff history, even with `--force`.

Subproject (top-level child; the repo root is the implicit parent):

```bash
python3 scripts/scaffold_project.py \
  --root /path/to/repo \
  --name "Agent Layer" \
  --slug agent-layer
```

Nested subproject (`--parent` names the ancestor by slug or projects path):

```bash
python3 scripts/scaffold_project.py \
  --root /path/to/repo \
  --parent agent-layer \
  --name "Agent Evals" \
  --slug evals
```

The script skips existing files by default. Use `--force` only when intentionally regenerating scaffold files. `--force` still preserves `.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, and `reference/README.md`, and appends to `.agents/log.md` rather than overwriting it.
