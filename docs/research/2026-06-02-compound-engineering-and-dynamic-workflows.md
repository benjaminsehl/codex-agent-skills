# Research: Compound Engineering & Dynamic Workflows

Last updated: 2026-06-02
Status: research synthesis (founder-shared references)
Informs: the measurement-first 10x roadmap (`docs/plans/2026-06-01-assembly-10x-roadmap.md`)

Two founder-shared references, and how they sharpen Assembly:

- Every Inc's **Compound Engineering** plugin — github.com/everyinc/compound-engineering-plugin
- Anthropic's **Dynamic Workflows** in Claude Code — claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code and code.claude.com/docs/en/workflows

## 1. Compound Engineering names Assembly's thesis

Core principle, near-verbatim our 10x thesis: **"Each unit of engineering work should make subsequent units easier — not harder."** 80% planning/review, 20% execution. Loop:
`strategy → ideate → brainstorm → plan → work → code-review → compound → repeat`, with a durable `STRATEGY.md` anchoring the upstream phases (our `product/` + north-star), and an explicit **`/ce-compound`** step that documents learnings for reuse *every cycle*, plus `/ce-product-pulse` timelines that feed strategy.

Takeaways:

- **Framing.** "Compounding loops" is a sharper external name for measurement-first. The course-correction ledger *is* a compounding mechanism.
- **The missing mechanism: a per-cycle `compound` step.** Compound engineering captures learnings after *every* unit, not just at end-of-project retro. Assembly should make this first-class: after each slice, write any new founder correction to the course-correction ledger and any reusable pattern to the lessons index. This upgrades Stage 1 (alignment) and the lessons-index connective tissue.
- **What NOT to copy.** They ship 37 skills + 51 agents. That is the opposite of Assembly's "few entrypoints, deep references" bet (and our capability-acquisition model, which assembles only the domain skills a stack needs). Borrow the mechanism and framing, not the surface area.

## 2. Dynamic Workflows are the execution substrate for the measurement loops

A dynamic workflow is **a JavaScript script that orchestrates subagents at scale** (dozens–hundreds), written by Claude for the task, run in the background by a runtime while the session stays responsive. The plan lives in the *script* — loop, branching, intermediate results — so the main context only sees the final answer. It can choose per-agent models and worktree isolation, and is resumable.

### The failure modes it combats (why isolated-context orchestration matters)

These are exactly what Assembly's measurement loops guard against:

- **Agentic laziness** — stopping after partial progress (35 of 50 review items) and declaring done.
- **Self-preferential bias** — preferring its own results when asked to verify/judge them. (This is precisely why agent-graded evals need a *separate* judge, and why a `vision-keeper` must be a distinct agent.)
- **Goal drift** — lossy compaction dropping edge-case and "don't do X" constraints over many turns.

Separate subagents with isolated context and focused goals structurally prevent these.

### Composable patterns (add to `orchestration-patterns.md`)

- **Classify-and-act** — a classifier routes to different agents/behavior (also model/intelligence routing).
- **Fan-out-and-synthesize** — split into many steps, one agent each, a synthesize barrier merges structured outputs.
- **Adversarial verification** — a separate agent verifies each agent's output against a rubric.
- **Generate-and-filter** — generate ideas, filter by rubric/verification, dedupe, return the best.
- **Tournament** — N agents attempt the same task different ways; pairwise judge to a winner (comparative judgment beats absolute scoring — useful for taste/sorting).
- **Loop-until-done** — spawn until a stop condition (no new findings, no errors), not a fixed count.

### Two use cases are Assembly's two measurement tracks, almost verbatim

- **Track A (course-correction ledger).** The blog's "mine your recent sessions and code-review comments for corrections you keep making → cluster with parallel agents → adversarially verify each candidate (*would this rule have prevented a real mistake?*) → distill survivors into CLAUDE.md rules" **is** ledger ingestion, automated. The iMessage/founder loop seeds it; this workflow mines it.
- **Track B (agent-graded evals).** The blog's "evals: spin off agents in a worktree, spin off comparison agents to grade outputs against a rubric — e.g. evaluating and refining a skill against criteria" **is** Stage 2's eval harness. Use a worktree per fixture run; a separate grader per rubric; a skeptic agent to limit false positives.

### Distribution: ship workflows inside skills

Workflows save to `~/.claude/workflows/` (press `s`) or **distribute via a skill** — put the JavaScript in the skill folder, reference it in `SKILL.md`, and treat it as a *template* rather than a verbatim script. This is how Assembly can ship `ship`, `review`, the eval runner, and the ledger-miner as workflows without leaving the skill surface. Pair repeatable ones (triage, eval, verification) with `/loop` and `/goal`; cap cost with a token budget ("use 10k tokens").

### When NOT to use

Most routine coding tasks do not need a workflow — they cost meaningfully more tokens. Reserve for complex, high-value, massively-parallel, or adversarial tasks. (This note itself did not warrant one.)

## Relationship to Hermes and capability-acquisition

- **Complementary to Hermes, not competing.** Dynamic workflows = in-session orchestration at scale; Hermes/OpenClaw = the always-on, cross-session operator. Stage 4 wants both: Hermes decides *what* runs and talks to the founder; a workflow executes the *scaled* step.
- **Capability-acquisition fit.** A workflow could fan out to assemble/validate the domain skills a detected stack needs, and the generate-and-filter / adversarial-verification patterns fit skill quality-gating.

## Recommended folds (made in this PR)

- `orchestration-patterns.md`: a Dynamic Workflows section (the six patterns, when-to-use vs subagents/skills/agent-teams, the failure modes, skill-distribution).
- `docs/plans/2026-06-01-assembly-10x-roadmap.md`: per-cycle `compound` step into Stage 1 + lessons index; dynamic workflows as the substrate for the Stage 2 eval runner and Stage 4; failure-modes framing.
