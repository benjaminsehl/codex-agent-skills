# Release Checklist: Assembly 1.0

Last updated: 2026-05-27
Status: draft

## Product Gate

- [ ] Founder accepts the 1.0 spec.
- [ ] Founder accepts the app-factory north star.
- [ ] 1.0 blockers are separated from post-1.0 orchestrator work.
- [ ] Product-discovery interview behavior is verified.
- [ ] `next` behavior is verified on a real project trail.

## Plugin Gate

- [ ] Codex manifest (`.codex-plugin/plugin.json`) name, version, description, and icon are correct.
- [ ] Claude Code manifest (`.claude-plugin/plugin.json`) name, version, description, and icon are correct.
- [ ] Marketplace metadata (`.claude-plugin/marketplace.json`) is correct.
- [ ] Only the candidate public skill surface (currently 13 skills) is exposed in both runtimes; any drift from that set is intentional and recorded.
- [ ] Skill graph validates.
- [ ] Plugin shape validates.
- [ ] Local conflict audit runs.
- [ ] Install and upgrade docs are accurate for both Codex and Claude Code.

## Project Scaffold Gate

- [ ] Root scaffold creates `AGENTS.md`, `.agents/`, `docs/`, and `reference/`.
- [ ] Existing `AGENTS.md` is not overwritten.
- [ ] Force scaffold preserves protected files and appends to `.agents/log.md`.
- [ ] Subproject scaffold creates `.agents/projects/<slug>/`.

## Behavior Gate

- [ ] `next` repairs stale or missing status before dispatching.
- [ ] `next` asks one concise question when multiple next actions are plausible.
- [ ] `build` with a minimal prompt infers the next unambiguous build-track gate.
- [ ] GitHub handoff creates or updates a descriptive PR, deciding draft vs ready as an engineering call.
- [ ] Ready-for-review proceeds autonomously once reviewer sub-agents are satisfied, verification is green, and no open product/UX decision remains — no founder approval required.
- [ ] Merge and deploy proceed autonomously when `Traffic state: pre-live`; when `live`, the agent prepares a GO/NO-GO and asks the founder before merging to the default branch, then deploy follows.
- [ ] Product/UX decisions are escalated to the founder in product-implication language and pause progress until answered.
- [ ] Always-ask floor is honored regardless of traffic state: money, credentials, external messaging, privacy-sensitive data, irreversible destructive ops, and merging to the default branch when live.

## Proof Gate

- [ ] Assembly self-host proof is complete.
- [ ] CFO proof is complete.
- [ ] Hyper retrofit proof is complete or explicitly deferred.
- [ ] Smoke-test evidence is recorded.
- [ ] Release retro is recorded.

## Release Gate

- [ ] Version is bumped.
- [ ] Release PR is approved.
- [ ] PR is merged after explicit founder approval.
- [ ] Local Codex plugin is upgraded.
- [ ] Local Claude Code plugin is upgraded.
- [ ] Fresh Codex session confirms Assembly skills are visible.
- [ ] Fresh Claude Code session confirms Assembly skills are visible.
- [ ] `Use next` works in the installed plugin in both runtimes.

## Current Verdict

NO-GO until spec acceptance, release-candidate implementation, real smoke evidence, and CFO proof are complete.
