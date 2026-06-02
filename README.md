# Assembly

Assembly is a founder-led product-building toolkit for an eventual agentic app factory: contextual next steps, project orientation, product discovery, prototypes, specs, plans, implementation, tests, QA, review, simplification, and release decisions.

The plugin ships as both a Codex plugin and a Claude Code plugin from the same bundle at `plugins/assembly/`. It intentionally exposes a small public skill surface; detailed guidance lives in the plugin bundle's `references/` directory so agents load it only when needed.

The founder stays product director. Assembly reserves founder attention for product/UX decisions — framed in user-facing terms — and runs engineering autonomously, validating it with reviewer sub-agents instead of per-PR approval. How far that autonomy reaches is set by the project's traffic state (see [Autonomy Model](#autonomy-model)).

## Quick Start

### Claude Code

Add the marketplace, then install the plugin:

```bash
/plugin marketplace add benjaminsehl/assembly
/plugin install assembly@assembly
```

If the marketplace is already registered:

```bash
/plugin marketplace update assembly
```

### Codex

Register the public marketplace:

```bash
codex plugin marketplace add benjaminsehl/assembly
```

If it is already registered:

```bash
codex plugin marketplace upgrade assembly
```

Migrating from the old name:

```bash
codex plugin marketplace remove codex-agent-skills
codex plugin marketplace add benjaminsehl/assembly
```

Then invoke public skills in natural language:

```text
Use next to do the next normal thing.
Use init to scaffold this repo (or a subproject).
Use project-status to tell me what phase we are in and what skills to use next.
Use product-discovery on this idea.
Use prototype before we build this direction.
Use spec to define this feature before coding.
Use plan to break the approved spec into tasks.
Use build to implement the next planned slice.
Use test to prove this bug.
Use qa on this local app.
Use review on the current diff.
Use code-simplify on the changed files.
Use ship to decide whether this is ready.
```

If you already have personal lifecycle skills installed, treat this plugin as the owner of that surface. Keep specialized platform skills, but de-duplicate older lifecycle skills named `next`, `init`, `spec`, `plan`, `build`, `test`, `review`, `ship`, `qa`, `prototype`, `product-discovery`, or `project-status`.

## Public Skills

| Skill | Job |
| --- | --- |
| `next` | Contextual continuation: inspect project state, choose the next normal action, and proceed when unambiguous |
| `init` | Scaffold a project or subproject workspace, including default Claude Code and Codex permission config |
| `project-status` | Project gateway for status, repair, retro, and next-skill routing (delegates scaffold to `init`) |
| `product-discovery` | Product gateway for raw ideas, founder critique, business viability, and design-plan pressure tests |
| `prototype` | Tangible proof before production build |
| `spec` | Requirements before coding |
| `plan` | Dependency-ordered tasks after spec |
| `build` | One verified implementation slice |
| `test` | Behavior proof, bug reproduction, and runtime checks |
| `qa` | User-like product testing after implementation |
| `review` | Diff, branch, commit, or PR review |
| `code-simplify` | Behavior-preserving cleanup |
| `ship` | Go/no-go release decision |

## Claude Code Enhancements

On Claude Code (not Codex), Assembly ships two additive surfaces beyond the shared skills. They degrade to nothing on Codex, which keeps the portable skill surface and its own approval policy.

- **Specialist subagents** — `code-reviewer`, `security-auditor`, and `test-engineer`, declared in `plugins/assembly/.claude-plugin/plugin.json` and defined in [`.agents/personas/`](plugins/assembly/.agents/personas/). `review` and `ship` fan out to them in parallel; each can run on a per-persona model.
- **Hooks** ([`plugins/assembly/hooks/`](plugins/assembly/hooks/)):
  - A **SessionStart primer** orients each session to `.agents/status.md`, the current phase, and the recommended next skills — silent outside Assembly projects.
  - An **ask-first PreToolUse guard** re-prompts before merges, deploys, force/main/delete pushes, publishes, and destructive shell ops — the runtime counterpart to the always-ask floor, so the scaffold's maximum default permissions stay safe.

## Current 1.0 Direction

- [Assembly 1.0 spec](.agents/specs/assembly-1-0.md)
- [App-factory north star](docs/product/app-factory-north-star.md)
- [1.0 release plan](.agents/plans/2026-05-27-assembly-1-0-release-plan.md)
- [Post-1.0 orchestrator roadmap](.agents/plans/2026-05-27-post-1-0-orchestrator-roadmap.md)
- [Agentic orchestration research](.agents/research/2026-05-27-agentic-orchestration-research.md)

## Project Docs Convention

The root project workspace splits by audience: the agent's operational trail lives under `.agents/` (status, phases, specs, plans, research, QA, release, evals) and human documentation under `docs/` (product, decisions, tech-design). Subprojects nest identically under `projects/<slug>/` in both trees and can recurse.

```text
my-app/
|-- AGENTS.md
|-- .claude/
|   `-- settings.json
|-- .codex/
|   `-- config.toml
|-- .agents/              # agent operational trail
|   |-- AGENT-GUIDANCE.md
|   |-- log.md
|   |-- notes/
|   |-- status.md
|   |-- phases/
|   |-- specs/
|   |-- plans/
|   |-- prototypes/
|   |-- research/
|   |-- qa/
|   |-- release/
|   `-- projects/
|-- docs/                 # human documentation
|   |-- README.md
|   |-- product/
|   |-- decisions/
|   |-- tech-design/
|   `-- projects/
|-- reference/
`-- src/
```

Why this shape:

- Markdown is split by audience: the operational trail the agent uses to do and resume work lives in `.agents/`; documents that help a human understand the product and the code live in `docs/`.
- `AGENTS.md` stays the top-level entrypoint; instruction-like files use uppercase names (`AGENT-GUIDANCE.md`) and records like `log.md` and `notes/` stay lowercase.
- Agents get one obvious place to start: `.agents/status.md`.
- Subprojects nest identically under `projects/<slug>/` in both trees.
- Chesterton's fence is visible before important decisions are changed.

## How Agents Should Work Through A Project

1. Use `next` when the user asks to continue through the normal process.
2. Read `.agents/status.md` and nearest subproject status.
3. Use `project-status` when the phase, scaffold, repair path, or next skill is not obvious.
4. Use `product-discovery` when product direction, user love, or business viability is unclear.
5. Choose the matching lifecycle skill for the current phase.
6. If prerequisites are missing, warn once and recommend the right double-back skill.
7. If the user insists, proceed while naming the skipped gate and risk unless a hard safety boundary applies.
8. For material changes in GitHub-backed repos, open a PR, run reviewer sub-agents and `code-simplify`, then promote to ready autonomously and merge per the traffic state — escalating only product/UX decisions and the live-traffic merge gate.

## Autonomy Model

Assembly decides what to escalate on two axes, not on phase ceremony:

- **Decision type.** Product and UX decisions — what gets built and why, user-facing behavior, copy, flow, scope cuts that change the experience, naming, pricing — always go to the founder in product-implication language. Engineering decisions run autonomously and are validated by reviewer sub-agents (`code-reviewer`, `security-auditor`, `test-engineer`), not by founder approval. Whether to open a draft PR, promote it to ready, or merge an engineering-only change is an engineering call, not an interruption.
- **Traffic state.** `.agents/status.md` carries a founder-set `Traffic state:` field (default `pre-live`). When `pre-live`, the agent runs the whole roadmap — multiple PRs, merges, and deploys — with no per-action check-in, as long as no product/UX decision is open. When `live`, opening PRs and review stay autonomous and merging to the default branch becomes a founder GO/NO-GO; deploy then follows the approved merge. (A release branch can later move this gate; until then, merge to the default branch is the live gate.)

The **always-ask floor** holds in any traffic state: money movement, credential use, external messaging, privacy-sensitive data, irreversible destructive operations, and merging to the default branch when live.

## GitHub Handoff

Assembly expects agents to leave real work reviewable, and to carry it forward without waiting on engineering approvals:

- `build` commits focused changes on a topic branch and pushes.
- `ship` opens or updates a descriptive PR (with `gh` or the GitHub MCP tools), deciding draft vs ready as an engineering call.
- Explain why the PR exists, the first principles behind the change, and how the agent approached it.
- Run `review` (reviewer sub-agent fan-out) and `code-simplify`, then promote to ready autonomously once verification is green and reviewers are satisfied.
- Merge and deploy autonomously when `pre-live`; when `live`, ask the founder GO/NO-GO before merging to the default branch, then let deploy follow the approved merge.
- When addressing PR comments, inspect review threads, implement traceable fixes, push updates, and reply/resolve threads as part of the engineering loop — escalating only threads that raise a product/UX decision.
- Honor the always-ask floor regardless of traffic state.

The canonical agent protocol lives in [references/agent-operating-protocol.md](plugins/assembly/references/agent-operating-protocol.md). New projects receive a copy at `.agents/AGENT-GUIDANCE.md`.

## Scaffolding

From this plugin checkout, scaffold a root project:

```bash
python3 plugins/assembly/scripts/scaffold_project.py --root /path/to/repo --name "Project Name"
```

Scaffold a subproject:

```bash
python3 plugins/assembly/scripts/scaffold_project.py \
  --root /path/to/repo \
  --name "Agent Layer" \
  --slug agent-layer
```

For a nested subproject, add `--parent <parent-slug>`.

The script skips existing files by default. If the target repo already has `AGENTS.md`, the scaffold will not overwrite it; merge [templates/AGENTS.md](plugins/assembly/templates/AGENTS.md) manually.

## Validation

```bash
python3 plugins/assembly/scripts/validate_plugin.py
python3 plugins/assembly/scripts/validate_skill_graph.py
python3 plugins/assembly/scripts/audit_skill_conflicts.py
python3 -m py_compile plugins/assembly/scripts/validate_plugin.py plugins/assembly/scripts/validate_skill_graph.py plugins/assembly/scripts/scaffold_project.py plugins/assembly/scripts/audit_skill_conflicts.py
```

## Source References

- Addy Osmani `agent-skills`: https://github.com/addyosmani/agent-skills
- Garry Tan `gstack`: https://github.com/garrytan/gstack
- Matt Pocock `skills`: https://github.com/mattpocock/skills
- Benjamin Sehl `agent-kernel`: https://github.com/benjaminsehl/agent-kernel
- Install details: [docs/INSTALL.md](plugins/assembly/docs/INSTALL.md)
- Source notes: [docs/SOURCE_NOTES.md](plugins/assembly/docs/SOURCE_NOTES.md)
