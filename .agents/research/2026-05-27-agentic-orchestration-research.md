# Research: Agentic Orchestration For Assembly

Last updated: 2026-05-27
Status: working synthesis

## Sources Reviewed

- Anthropic, "Building effective agents" (2024-12-19): https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, "How we built our multi-agent research system" (2025): https://www.anthropic.com/engineering/multi-agent-research-system
- OpenAI, "Agents SDK" docs: https://developers.openai.com/api/docs/guides/agents
- OpenAI Agents SDK, "Guardrails" docs: https://openai.github.io/openai-agents-python/guardrails/
- Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering" (2024): https://arxiv.org/abs/2405.15793
- Model Context Protocol specification: https://modelcontextprotocol.io/specification/2024-11-05/basic

## Synthesis

The strongest production advice is to start with simple, inspectable workflows and add autonomy only where the task value justifies the complexity.

Assembly should therefore treat `next`, phase gates, status repair, GitHub handoff, and project-local evidence as the core runtime. A post-1.0 orchestrator should come later as a coordinator over these visible workflows, not as an opaque replacement for them.

## Implications For Assembly

### Keep The Control Loop Simple

The 1.0 loop should be:

```text
read trail -> classify phase -> identify missing context -> ask or dispatch -> act -> verify -> hand off -> update trail
```

That loop is easier to debug than an autonomous planner with hidden state.

### Design For Agent-Computer Interfaces

The repo structure is an interface for agents. `.agents/status.md`, `.agents/log.md`, specs, plans, decisions, QA notes, release notes, and PRs should be easy for agents to inspect without loading the whole repository.

### Use Multi-Agent Work Sparingly

Multi-agent fanout is useful when work can be separated cleanly: research, review, QA, security, release readiness, or context audits.

It is less useful when tasks share lots of mutable code context or require tight real-time coordination. For most coding work, one owner should hold the patch while sidecar agents review, research, or test.

### Keep The Founder In Judgment Gates

Founder/product-director questions are not interruptions. They are the control surface.

Assembly should ask when the project lacks:

- What is being built.
- Why it matters.
- What good looks like.
- Which tradeoffs are acceptable.
- Whether to proceed through release, merge, deploy, destructive, privacy, or money boundaries.

### Require Evidence And Guardrails

Assembly should keep ask-first boundaries explicit and local:

- Product judgment missing: ask before deciding.
- Risky tool call: ask before acting.
- Draft PR ready-for-review: ask first.
- Merge or deploy: ask first.
- Unresolved comments/checks: stop or name the accepted risk.

Future orchestrator work should preserve those boundaries as typed guardrails, not just prose.

## Near-Term Roadmap Guidance

1. Ship Assembly 1.0 as a dual-runtime plugin (Codex and Claude Code) and project protocol.
2. Prove it on Assembly and CFO.
3. Capture real smoke evidence in both runtimes.
4. Define a post-1.0 orchestrator contract around project status, skill invocation, work ownership, evidence, and approval boundaries.
5. Build a post-1.0 orchestrator alpha only after the agent control loop feels boringly reliable.

## Open Questions

- What structured format should the post-1.0 orchestrator use to represent phase state and next actions?
- Should Assembly status remain pure markdown, or should it grow a small machine-readable frontmatter block?
- What evidence should the post-1.0 orchestrator require before spawning another agent session?
- Which gates should always pause for founder input, even if a future orchestrator thinks the answer is obvious?
