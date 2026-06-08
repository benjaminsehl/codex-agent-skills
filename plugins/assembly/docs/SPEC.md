# Spec: Assembly Plugin

## Objective

Build a compact agent plugin that acts as a personal product-building stack. It ships dual-target manifests so the same bundle works in both Codex and Claude Code, and should help future agents continue to the next contextual step, orient a project, shape product direction, prototype, specify, plan, build, test, QA, review, simplify, and ship with evidence.

The public surface is intentionally small. Detailed workflow knowledge lives in `references/` so agents load it only when needed and avoid conflicts with users' existing skills.

## Public Skill Surface

| Public skill | Job | Key references |
| --- | --- | --- |
| `next` | Continue through the normal process by choosing the next evidence-backed action | `project-phases`, `agent-operating-protocol`, `workflows/project-lifecycle` |
| `init` | Scaffold a project or subproject workspace via `scripts/scaffold_project.py`, including default Claude Code and Codex permission config | `project-kernel-structure`, `workflows/project-lifecycle`, `project-phases`, `agent-operating-protocol` |
| `project-status` | Project gateway for status, repair, retro, and next-skill routing (delegates scaffold to `init`) | `project-phases`, `project-kernel-structure`, `agent-operating-protocol`, `workflows/project-lifecycle` |
| `product-discovery` | Product gateway for ideas, founder critique, business viability, and design-plan critique | `product-discovery-checklist`, `business-model-checklist`, `design-quality-checklist`, `workflows/product-strategy` |
| `prototype` | Create tangible throwaway evidence before production build | `workflows/product-strategy`, `project-phases` |
| `spec` | Define what to build before coding | `workflows/engineering-delivery`, `project-phases` |
| `plan` | Convert approved requirements into small verifiable tasks | `workflows/engineering-delivery`, `project-phases` |
| `build` | Implement one planned slice with tests and verification | `workflows/engineering-delivery`, `testing-patterns` |
| `test` | Prove behavior with tests and runtime checks | `workflows/engineering-delivery`, `testing-patterns` |
| `qa` | Test the product like a user after implementation | `qa-checklist`, `workflows/qa-and-release` |
| `review` | Review current changes before merge | `workflows/engineering-delivery`, `security`, `performance`, `accessibility` checklists |
| `code-simplify` | Reduce complexity without changing behavior | `workflows/engineering-delivery`, `testing-patterns` |
| `ship` | Produce a go/no-go launch decision | `workflows/qa-and-release`, release checklists |

Success means a future agent session in either Codex or Claude Code can invoke one of these skills by name, load only the necessary references, and produce consistent evidence across three lenses: users love it, engineering is excellent, and the business model is viable.

For GitHub-backed implementation work, success also means the agent leaves changes in a reviewable PR workflow: focused commits, pushed branch, a PR, self-review, simplification pass, and verification evidence. Opening the PR, choosing draft vs ready, and promoting to ready are engineering calls the agent makes autonomously, validated by reviewer sub-agents rather than founder approval. The founder's attention is reserved for product/UX decisions and, when traffic state is `live`, the merge-to-default-branch gate.

## Project Phase Model

Every full project or substantial project slice follows four phases:

1. **Proposal:** define what becomes 10x better, what good looks like, outcomes, assumptions, principles, risks, and non-goals.
2. **Prototype:** create tangible proof or playable artifacts before committing to production build direction.
3. **Build:** implement approved slices with specs, plans, tests, reviews, and tech-design updates.
4. **Release:** run QA and polish, decide go/no-go, ship or hold intentionally, grade against proposal, and capture follow-up learning.

Projects are recursive. A repo can be a project, and clients, agent layers, releases, or features inside it can be subprojects with their own phase trail under `.agents/projects/<slug>/`.

Agent-only operating material belongs under `.agents/`, with root `AGENTS.md` kept as the visible entrypoint. The scaffold writes the reusable operating protocol to `.agents/AGENT-GUIDANCE.md` and keeps raw source material in top-level `reference/`.

## Validation

Required commands from the repository root:

```bash
python3 plugins/assembly/scripts/validate_plugin.py
python3 plugins/assembly/scripts/validate_skill_graph.py
python3 plugins/assembly/scripts/audit_skill_conflicts.py
python3 -m py_compile plugins/assembly/scripts/validate_plugin.py plugins/assembly/scripts/validate_skill_graph.py plugins/assembly/scripts/scaffold_project.py plugins/assembly/scripts/audit_skill_conflicts.py
git diff --check
```

Validation must ensure:

- Only the 13 public skills are triggerable from this plugin.
- Public skills have concise descriptions, required sections, and direct reference links.
- Public skills do not list deleted support skills as dependencies.
- Required references, templates, personas, and scaffold scripts exist.
- Install docs explain existing skill conflicts and replacement guidance.
- GitHub handoff guidance explains `gh` usage, draft PRs, existing-PR updates, blocked-handoff fallback, self-review, code simplification, PR review feedback, and ask-first ready-for-review gates.
- Scaffolds create `.agents/AGENT-GUIDANCE.md`, `.agents/log.md`, `.agents/notes/`, and `reference/` while avoiding `docs/agent-guidance.md`.
- Scaffolds create `.claude/settings.json` (Claude Code `bypassPermissions`) and `.codex/config.toml` (Codex `approval_policy = "never"`, `sandbox_mode = "danger-full-access"`) so both runtimes get maximum default permissions, and preserve either file when it already exists.
- Scaffold force mode preserves `.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, and `reference/README.md`, and appends to `.agents/log.md` instead of overwriting agent instructions, support guidance, or handoff history.
- References over 100 lines include a `## Contents` section.

## Boundaries

Always:

- Prefer project conventions over generic workflow.
- Keep public skills thin.
- Put detailed guidance in `references/`.
- Preserve a decision paper trail.
- Validate before calling the plugin install-ready.
- Leave material GitHub-backed work in a reviewable PR unless the user asks for local-only changes.
- Escalate product/UX decisions to the founder in product-implication language; decide engineering autonomously and validate it with reviewer sub-agents.
- Read the `Traffic state:` field in `.agents/status.md` before merging, deploying, or shipping; treat absent or unknown as `pre-live`.

Autonomy by traffic state:

- `pre-live` (default): with no open product/UX decision and no always-ask floor item, run the roadmap end to end — open PRs (draft or ready, agent's call), run reviewer sub-agents, merge, and deploy — without per-action approval.
- `live`: opening PRs, reviewing, and readying stay autonomous; merging to the default branch is a founder GO/NO-GO, and deploy follows the approved merge.

Always-ask floor (any traffic state):

- Before overwriting existing `AGENTS.md`.
- Before destructive operations, external messaging, money movement, credential use, or privacy-sensitive work.
- Before irreversible destructive git operations (force-push to default branch, deleting branches with unmerged work).
- Before merging to the default branch when traffic state is `live`.
- Before skipping phase gates when risk materially changes.

On the Claude Code runtime, the `ask-first-guard.sh` PreToolUse hook enforces this floor at the shell boundary: it reads the same `Traffic state:` field — so a `pre-live` project's PRs, merges, and deploys pass unprompted while `live` re-gates merge-to-default and deploy — and is tunable per class via `ASSEMBLY_ASK_FIRST_*` environment variables (see `hooks/README.md`). Codex relies on the prose floor and its own approval policy.

Never:

- Expose broad triggerable support skills that collide with common user skills.
- Treat business or product assumptions as proven without evidence.
- Mark work complete without verification.
