# Research: OpenClaw / Hermes as an Assembly Runtime

Last updated: 2026-06-01
Status: research synthesis (founder uses an OpenClaw instance named "Hermes")
Scope: informs Loop 4 (autonomous operations) of the 10x roadmap

## Why this note exists

The founder runs an always-on personal agent on his computer named **Hermes**.
Hermes is an instance of **OpenClaw**. The founder wants to fully delegate
low-oversight projects to Hermes and steer them by chatting over iMessage. This
note records what OpenClaw is and how Assembly should relate to it, so the Loop 4
("autonomous operations") direction builds on what already exists instead of
reinventing it.

## What OpenClaw is

OpenClaw (Peter Steinberger; MIT-licensed; very large, fast-growing OSS project)
is a self-hosted, always-on personal AI agent.

- **Daemon.** `openclaw onboard --install-daemon` installs a launchd/systemd
  user service that runs 24/7. Workspace at `~/.openclaw/workspace`, config at
  `~/.openclaw/openclaw.json`.
- **Multi-channel inbox.** 20+ messaging platforms including **iMessage**,
  WhatsApp, Telegram, Signal, Slack, Discord. Unknown senders get a DM pairing
  code; approval adds them to a local allowlist. This is the founder's
  iMessage channel.
- **Standing rules via injected prompt files.** `SOUL.md` (personality +
  operating guidelines), `AGENTS.md`, and `TOOLS.md` in the workspace root shape
  behavior. SOUL.md is where an operator gives the agent durable character and
  rules.
- **Persistent memory + sessions.** Per-agent session state; survives restarts;
  `/reset`, `/compact`.
- **Skills.** `~/.openclaw/workspace/skills/<skill>/SKILL.md`, plus a ClawHub
  registry. **Same `SKILL.md` + YAML-frontmatter (`name`, `description`) format
  Assembly uses.**
- **Autonomy.** Main session runs at full access; non-main/group sessions can be
  sandboxed (Docker/SSH/restricted tool allowlists).

**"Hermes" = the founder's OpenClaw instance** — a named, always-on agent with
its own SOUL.md, reachable over iMessage.

## The relevant bridge already exists

`goldmar/openclaw-code-agent` runs **Claude Code and Codex as managed background
coding sessions launched from chat**:

- Flow: **Launch → Plan Review → Execution → Follow-Through → Chat
  Notification.**
- **Autonomy modes** (these map onto Assembly's escalation model):
  - `plan` — proposes a plan, waits for approval.
  - `delegate` (default) — orchestrator reviews the finished worktree and
    auto-merges.
  - `ask` — interactive Merge / Open PR / Later / Discard buttons in chat.
  - `off` — direct execution.
- **Worktree isolation**, branch/PR follow-through, cost tracking
  (`agent_stats`, USD), and one concise factual update back to the originating
  chat thread.
- Configured in the `~/.openclaw/openclaw.json` plugin block (`defaultWorkdir`,
  `defaultHarness`, `permissionMode`, `planApproval`, `defaultWorktreeStrategy`,
  `agentChannels`).

This is substantially the "post-1.0 orchestrator" role Assembly has described
generically — already built. It rhymes with the dropped 2026-05-23 decision,
which framed *"Hermes as the product/roadmap operator, Codex as the focused
builder executing Assembly-scoped work."*

## Implications for Assembly

1. **Hermes is a third runtime target, cheaply.** Assembly already ships
   dual-runtime (Codex + Claude Code) from one `SKILL.md` bundle. OpenClaw uses
   the same format and installs skills into the same `~/.codex/skills` /
   `~/.claude/skills` paths Assembly's `audit_skill_conflicts.py` already scans.
   Assembly can become a Hermes skill bundle plus a SOUL.md that loads the
   Assembly operating protocol as Hermes's standing rules.

2. **The oversight dial already exists in Hermes** — `plan`/`delegate`/`ask`/
   `off`. Assembly's job is to map its escalation model
   (decision-type × traffic-state × the proposed oversight axis) onto those
   modes: a low-oversight project runs `delegate`; a project the founder wants
   to steer runs `plan`/`ask`. The always-ask floor still overrides regardless
   of mode.

3. **The measurement loops are what make `delegate` safe on *product* work.**
   OpenClaw provides the autonomy mechanism (auto-merge from chat). On its own,
   aiming that at product decisions produces autonomous slop. The
   course-correction ledger (encoded taste) + vision-keeper + agent-graded
   evals are the safety that lets the founder turn `delegate` up per project.
   The loop closes over iMessage: when Hermes hits a novel product fork it
   texts the founder a product-implication question; the answer becomes a new
   ledger entry. **The iMessage thread is the ledger's ingestion point.**

4. **There is a real collision surface, not only synergy.** Assembly and
   OpenClaw both write `SKILL.md` into the same skill directories. The conflict
   audit must understand the Hermes namespace, and SOUL.md/AGENTS.md/TOOLS.md
   precedence vs. Assembly's `AGENTS.md` needs a defined ordering.

## Open questions

- Is "Hermes" adopted as the name for the Assembly-on-OpenClaw runtime target,
  or does it stay the founder's private instance name while Assembly refers to
  "the OpenClaw runtime"? (The 2026-05-28 drop-Hermes decision asked any
  name revival to land as its own decision with explicit reasoning — the
  messaging interface now supplies that reasoning if the founder wants it.)
- How do SOUL.md / TOOLS.md and Assembly's `AGENTS.md` compose without
  conflicting instructions?
- Does Assembly target the `openclaw-code-agent` plugin's autonomy modes
  directly, or define its own mapping layer on top?
- Which always-ask floor items need reinforcing when the operator is an
  auto-merging daemon (e.g. external messaging to third parties vs. messaging
  the founder)?

## Sources

- github.com/openclaw/openclaw
- github.com/goldmar/openclaw-code-agent
- github.com/openclaw/agent-skills
- digitalocean.com/resources/articles/what-is-openclaw
- milvus.io OpenClaw guide
