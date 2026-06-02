# Install and Use

This plugin ships dual-target manifests so a single bundle works as both a Codex plugin and a Claude Code plugin. It is intended to replace loose lifecycle skills with one coherent product-building stack.

The repository root is the marketplace. The installable plugin bundle lives at `plugins/assembly/`, matching both Codex's `./plugins/<plugin-name>` layout and Claude Code's marketplace layout. The bundle carries two manifest files in sibling metadata directories:

- `plugins/assembly/.codex-plugin/plugin.json` — Codex manifest.
- `plugins/assembly/.claude-plugin/plugin.json` — Claude Code manifest.

The marketplace catalogs are also dual:

- `.agents/plugins/marketplace.json` — Codex marketplace catalog.
- `.claude-plugin/marketplace.json` — Claude Code marketplace catalog.

## Register the Marketplace

### Claude Code

From inside Claude Code:

```text
/plugin marketplace add benjaminsehl/assembly
/plugin install assembly@assembly
```

If the marketplace is already registered and you want to pull updates:

```text
/plugin marketplace update assembly
```

For a local checkout, point the marketplace command at the repo path instead of the GitHub slug.

### Codex

From this local checkout:

```bash
codex plugin marketplace add /Users/sai/assembly
```

From GitHub:

```bash
codex plugin marketplace add benjaminsehl/assembly
```

The marketplace name is `assembly`.

If you previously installed the plugin under its old `codex-agent-skills` name, remove that marketplace first:

```bash
codex plugin marketplace remove codex-agent-skills
codex plugin marketplace add benjaminsehl/assembly
```

## Enable the Plugin

### Claude Code

`/plugin install assembly@assembly` enables the plugin in the current scope (defaults to user). Restart the session if the skill list does not refresh automatically.

### Codex

Enable `Assembly` from the plugin picker after adding the marketplace, then restart Codex so the skill list refreshes.

If enabling manually through config is needed, the expected config key shape is:

```toml
[plugins."assembly@assembly"]
enabled = true
```

## Existing Skill Conflicts

This plugin is intended to own lifecycle entry skills. Public entry skills:

`next`, `init`, `project-status`, `product-discovery`, `prototype`, `spec`, `plan`, `build`, `test`, `qa`, `review`, `code-simplify`, `ship`.

If you already have skills with these names, choose one owner before enabling this plugin:

- Recommended: keep this plugin enabled as the lifecycle owner, and disable or rename older skills with the same names.
- Keep specialized skills that do not overlap, such as framework, platform, browser, GitHub, Cloudflare, iOS, macOS, or design-system skills.
- Do not keep two active skills with the same entry name unless you are comfortable with ambiguous trigger behavior.

Run the advisory conflict audit:

```bash
python3 plugins/assembly/scripts/audit_skill_conflicts.py
```

## Replacing A Loose Skill Set

Suggested migration:

1. Register and enable `assembly` in your agent runtime.
2. Restart the runtime and confirm the public entry skills appear.
3. In a throwaway repo, run `Use next...`, `Use project-status...`, and `Use spec...`.
4. Disable, remove, or rename older lifecycle skills that collide with this plugin's entry names.
5. Keep specialized non-overlapping skills.
6. In project `AGENTS.md`, state that lifecycle routing should use Assembly.

## Invocation Pattern

Skills are invoked by name in natural language. In Claude Code each public skill is also available as a `/<name>` slash command; in Codex use the natural-language form. Either way, the workflows are the same:

```text
Use next to do the next normal thing.
Use init to scaffold this repo (or a subproject).
Use project-status to tell me what phase we are in and what skills to use next.
Use product-discovery on this idea.
Use prototype to explore this direction before build.
Use spec to define this feature before coding.
Use plan to break the approved spec into tasks.
Use build to implement the next planned slice.
Use test to prove this bug and guard against regression.
Use qa on this local app.
Use review to check the current diff.
Use code-simplify on the changed files.
Use ship to make a go/no-go release decision.
```

## Scaffolding

The recommended path is the `init` skill: invoke it in natural language (or `/init` in Claude Code) and it will run the scaffold script with the right flags for a root project, subproject, or nested subproject.

For deterministic project scaffolding directly from a checkout:

```bash
python3 plugins/assembly/scripts/scaffold_project.py --root /path/to/repo --name "Project Name"
```

For a child project inside an existing project workspace:

```bash
python3 plugins/assembly/scripts/scaffold_project.py \
  --root /path/to/repo \
  --name "Agent Layer" \
  --slug agent-layer
```

For a nested subproject, add `--parent <parent-slug>`.

If `AGENTS.md` already exists, the scaffold reports a manual merge notice instead of overwriting it. Review `plugins/assembly/templates/AGENTS.md` and merge the phase-aware protocol into the existing project instructions by hand.

The scaffold writes the operational trail to `.agents/` and human docs to `docs/`. Root-level agent material stays put:

- Root `AGENTS.md` stays as the visible entrypoint.
- `.agents/AGENT-GUIDANCE.md` receives the reusable operating protocol.
- `.agents/log.md` and `.agents/notes/` hold agent handoff context.
- `reference/` holds raw source material that should stay close to the project.

`--force` refreshes scaffold docs but still preserves existing `.agents/AGENT-GUIDANCE.md`, `.agents/notes/README.md`, and `reference/README.md`, and appends to `.agents/log.md` instead of overwriting agent instructions, support guidance, or handoff history.
