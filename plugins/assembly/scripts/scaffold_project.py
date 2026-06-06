#!/usr/bin/env python3
"""Create a project lifecycle workspace inside a target repository.

Audience split (see references/project-kernel-structure.md): operational
artifacts the agent uses to do and resume work live under `.agents/`; documents
written to help a human understand the product and the code live under `docs/`.
The two trees nest identically under `projects/<slug>/` for subprojects.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]

CLAUDE_SETTINGS = """{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
"""

CODEX_CONFIG = """# Assembly default permissions: maximum autonomy for Codex.
# Codex loads project .codex/ layers only for projects you have trusted,
# so trust this folder once to let these defaults apply.
approval_policy = "never"
sandbox_mode = "danger-full-access"
"""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "project"


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def projects_suffix(parent_slugs: list[str], slug: str) -> Path:
    """Build the projects/<...>/<slug> nesting shared by both trees."""
    suffix = Path()
    for parent in parent_slugs:
        suffix = suffix / "projects" / parent
    return suffix / "projects" / slug


def parse_parent(value: str) -> list[str]:
    """Parse --parent into an ordered list of ancestor slugs.

    Accepts a slug (``agent-layer``), a projects path
    (``projects/agent-layer/projects/api``), or a tree-prefixed path
    (``.agents/projects/agent-layer`` or ``docs/projects/agent-layer``). The
    repo root project is the empty list, so a top-level subproject needs no
    --parent.
    """
    cleaned = value.strip()
    # Tolerate an explicit tree prefix so both .agents/ and docs/ forms resolve.
    cleaned = re.sub(r"^[\\/]*(?:\.agents|docs)(?=[\\/])", "", cleaned)
    tokens = [tok for tok in re.split(r"[\\/]+", cleaned) if tok and tok != "projects"]
    return [slugify(tok) for tok in tokens]


def resolve_parent_chain(value: str, root: Path) -> list[str]:
    parent_slugs = parse_parent(value)
    if not parent_slugs:
        raise SystemExit("--parent did not name any ancestor project slug")
    ops_parent = root / ".agents" / projects_suffix(parent_slugs[:-1], parent_slugs[-1])
    if not (ops_parent / "status.md").is_file():
        raise SystemExit(
            f"Parent project workspace must contain status.md: {rel(ops_parent, root)}"
        )
    return parent_slugs


def load_required_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"Required scaffold template is missing: {path}")


def template_files(
    project_name: str,
    ops_dir: Path,
    docs_dir: Path,
    root: Path,
    protocol_text: str,
) -> dict[Path, str]:
    """Return scaffold files keyed by path.

    Operational files (status, phases, specs, plans, prototypes, research, qa,
    release, child-project container) go under ``ops_dir`` (``.agents``). Human
    documents (README, product, decisions, tech-design) go under ``docs_dir``
    (``docs``). Root-level agent infrastructure is keyed off ``root``.
    """
    today = date.today().isoformat()
    status_path = rel(ops_dir / "status.md", root)
    readme_path = rel(docs_dir / "README.md", root)
    phases_path = rel(ops_dir / "phases", root)
    projects_ops_path = rel(ops_dir / "projects", root)
    agent_guidance_path = rel(root / ".agents" / "AGENT-GUIDANCE.md", root)

    files: dict[Path, str] = {
        # ----- Human documents (docs/) -----
        docs_dir / "README.md": f"""# {project_name}

Human-facing documentation for this project: what it is, why it matters, and how
the code works. The agent's operational trail (status, phases, specs, plans, QA,
release, research) lives under `.agents/`.

Start here:

- Current status (agent trail): `{status_path}`
- Phase model (agent trail): `{phases_path}/`
- Decisions: `decisions/`
- Product vision: `product/vision.md`
- Tech design: `tech-design/`
- Agent guidance: top-level `AGENTS.md` and `{agent_guidance_path}`
- Child projects: `{projects_ops_path}/` (agent trail) and matching `docs/.../projects/` (human docs)
""",
        docs_dir / "product" / "vision.md": f"""# Product Vision: {project_name}

## User

Who this is for.

## Painful Moment

The moment that makes this project matter.

## Promise

The user-visible promise this project should keep.

## Non-Goals

- TBD
""",
        docs_dir / "product" / "principles.md": """# Product Principles

Principles that should shape decisions throughout the project.

- TBD
""",
        docs_dir / "decisions" / "README.md": """# Decisions

Use this folder for decisions that are hard to reverse, surprising without context, and the result of a real trade-off.

## Decision Record Template

```markdown
# YYYY-MM-DD Decision Title

## Status

Proposed | Accepted | Replaced

## Context

What forced the decision?

## Options Considered

- TBD

## Decision

What did we choose?

## Why This Wins

Why is this best for the project outcomes and principles?

## Consequences

What gets easier, harder, or riskier?
```
""",
        docs_dir / "tech-design" / "README.md": """# Tech Design

Capture architecture, interfaces, data model, runtime constraints, performance constraints, security constraints, and migration notes.

Prefer short design notes linked to specs, plans, and decisions.
""",
        # ----- Operational trail (.agents/) -----
        ops_dir / "status.md": f"""# Project Status: {project_name}

Last updated: {today}
Current phase: proposal
Traffic state: pre-live

## Phase Verdict

- Current phase: proposal
- Why: initial scaffold created; proposal outcomes and assumptions still need alignment.
- Next gate: proposal accepted by the user.

## Autonomy

- Traffic state: pre-live (no real users yet). The agent runs the roadmap autonomously — PRs, merges, deploys — escalating only product/UX decisions and always-ask floor items. Set `Traffic state: live` once real users depend on this; merging to the default branch then becomes a founder GO/NO-GO (deploy follows the approved merge).

## Next Recommended Skills

- `product-discovery`
- `spec`

## Open Questions

- Who is the target user?
- What becomes 10x better if this project succeeds?
- What does good look like at release?
- Which assumptions are riskiest?
""",
        ops_dir / "phases" / "proposal.md": """# Proposal Phase

## What Becomes 10x Better

Describe the user-visible improvement this project must create.

## What Good Looks Like

Define the observable outcome at the end of the project.

## Desired Outcomes

- TBD

## Assumptions

- TBD

## Principles

- TBD

## Risks

- TBD

## Decision Gate

Proposal is ready to leave this phase when outcomes, assumptions, principles, and success criteria are explicit enough to judge future work against them.
""",
        ops_dir / "phases" / "prototype.md": """# Prototype Phase

## Prototype Question

What must we learn or feel before production build work is justified?

## Tangible Artifacts

- TBD

## What Must Feel True

- TBD

## Findings

- TBD

## Decision Gate

Prototype is ready to leave this phase when it proves, changes, or rejects the proposed direction.
""",
        ops_dir / "phases" / "build.md": """# Build Phase

## Approved Direction

Link to the accepted proposal, prototype verdict, and spec.

## Implementation Slices

- TBD

## Acceptance Criteria

- TBD

## Verification

- TBD

## Risks

- TBD

## Decision Gate

Build is ready to leave this phase when production behavior is implemented, verified, and ready for QA and release polish.
""",
        ops_dir / "phases" / "release.md": """# Release Phase

## QA Scope

- TBD

## Polish Checklist

- TBD

## Ship Decision

- Verdict:
- Evidence:
- Rollback:

## Grade Against Proposal

- What became 10x better:
- What good looked like:
- Result:

## Follow-Up Work

- TBD

## Decision Gate

Release is done when the work is shipped or intentionally held, graded against the original proposal, and follow-up learning is captured.
""",
        ops_dir / "specs" / "README.md": """# Specs

Save approved behavior specs here. Specs should define user-visible behavior, constraints, acceptance criteria, and verification.
""",
        ops_dir / "plans" / "README.md": """# Plans

Save implementation plans here. Plans should break approved specs into small verifiable slices with explicit checks.
""",
        ops_dir / "prototypes" / "README.md": """# Prototypes

Save prototype notes and links here. Prototype code should stay clearly temporary and should be deleted or absorbed after the verdict is captured.
""",
        ops_dir / "research" / "README.md": """# Research

Save user, market, source, and technical research here. Separate observed evidence from assumptions.
""",
        ops_dir / "qa" / "README.md": """# QA

Save QA plans, tested flows, bugs, repro steps, evidence, and regression recommendations here.
""",
        ops_dir / "release" / "README.md": """# Release

Save launch checklists, ship decisions, rollout notes, rollback plans, and post-release grading here.
""",
        ops_dir / "projects" / "README.md": """# Child Projects

Use this folder for the operational trail of nested projects that belong inside this project boundary.

Create a child project here when the work needs its own proposal, prototype, build, and release trail. Its human documents live under the matching `docs/.../projects/<slug>/`.
""",
    }

    # Root-level agent infrastructure is created once, keyed off the repo root.
    files[root / ".agents" / "AGENT-GUIDANCE.md"] = protocol_text
    files[root / ".agents" / "log.md"] = f"""# Agent Log

Append meaningful agent handoff events, skipped gates, recovery notes, and project-operation changes here.

## {today}

- Project workspace scaffolded for `{project_name}`.
"""
    files[root / ".agents" / "notes" / "README.md"] = """# Agent Notes

Use dated notes for temporary agent working context, open loops, and handoff breadcrumbs.

Promote durable operational context into the project trail under `.agents/`, and durable product, design, or architecture context that helps a human into `docs/`. Keep raw source material in `reference/`.
"""
    files[root / "reference" / "README.md"] = """# Reference

Store raw source material, imports, screenshots, transcripts, datasets, vendor docs, and other evidence that should remain close to the project but should not be rewritten as project documentation.

When a reference changes a decision, summarize the durable conclusion in `docs/decisions/` (the human rationale) or the relevant `.agents/research/` or phase file (the agent trail).
"""
    return files


def write_files(
    files: dict[Path, str],
    root: Path,
    force: bool,
    protected_paths: set[Path],
) -> dict[str, list[str]]:
    created: list[str] = []
    skipped: list[str] = []

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and (not force or path in protected_paths):
            skipped.append(rel(path, root))
            continue
        path.write_text(content, encoding="utf-8")
        created.append(rel(path, root))

    return {"created": created, "skipped": skipped}


def append_log_entry(
    log_path: Path,
    root: Path,
    project_name: str,
    project_dir: Path,
    force: bool,
    result: dict[str, list[str]],
) -> None:
    if not log_path.is_file():
        result["skipped"].append(rel(log_path, root))
        result.setdefault("manual_merge", []).append(
            ".agents/log.md exists but is not a file; preserved and not updated. Replace it with a file to enable scaffold log entries."
        )
        return

    today = date.today().isoformat()
    mode = "force-refreshed" if force else "scaffolded"
    entry = (
        f"\n## {today}\n\n"
        f"- Project workspace {mode} for `{project_name}` at `{rel(project_dir, root)}`.\n"
    )
    text = log_path.read_text(encoding="utf-8")
    separator = "" if text.endswith("\n") else "\n"
    log_path.write_text(f"{text}{separator}{entry}", encoding="utf-8")
    result.setdefault("updated", []).append(rel(log_path, root))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold the .agents/ (operational) and docs/ (human) trees for a project workspace."
    )
    parser.add_argument("--root", default=".", help="Target repository root.")
    parser.add_argument("--name", default="", help="Human-readable project name.")
    parser.add_argument(
        "--slug",
        default="",
        help="Project slug. If provided, files are created under projects/<slug>/ in both trees.",
    )
    parser.add_argument(
        "--parent",
        default="",
        help=(
            "Existing ancestor subproject to nest under, named by slug or projects path "
            "(for example agent-layer or projects/agent-layer). Requires --slug. "
            "Omit for a top-level subproject; the repo root is the implicit parent."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing scaffold files.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Target root does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Target root is not a directory: {root}")

    project_name = args.name.strip() or args.slug.strip() or "Project"
    protocol_text = load_required_text(PLUGIN_ROOT / "references" / "agent-operating-protocol.md")
    agents_template = load_required_text(PLUGIN_ROOT / "templates" / "AGENTS.md")

    if args.parent.strip() and not args.slug.strip():
        raise SystemExit("--parent requires --slug so the child project has a stable path")

    if args.slug.strip():
        slug = slugify(args.slug.strip())
        parent_slugs = (
            resolve_parent_chain(args.parent.strip(), root) if args.parent.strip() else []
        )
        suffix = projects_suffix(parent_slugs, slug)
        ops_dir = root / ".agents" / suffix
        docs_dir = root / "docs" / suffix
    else:
        ops_dir = root / ".agents"
        docs_dir = root / "docs"

    files = template_files(project_name, ops_dir, docs_dir, root, protocol_text)
    agent_guidance_path = root / ".agents" / "AGENT-GUIDANCE.md"
    agent_guidance_exists = agent_guidance_path.exists()
    agent_notes_readme_path = root / ".agents" / "notes" / "README.md"
    agent_notes_readme_exists = agent_notes_readme_path.exists()
    reference_readme_path = root / "reference" / "README.md"
    reference_readme_exists = reference_readme_path.exists()
    log_path = root / ".agents" / "log.md"
    log_exists = log_path.exists()
    if log_exists:
        files.pop(log_path, None)

    agents_path = root / "AGENTS.md"
    agents_exists = agents_path.exists()
    if not agents_exists:
        files[agents_path] = agents_template

    claude_settings_path = root / ".claude" / "settings.json"
    claude_settings_exists = claude_settings_path.exists()
    if not claude_settings_exists:
        files[claude_settings_path] = CLAUDE_SETTINGS

    codex_config_path = root / ".codex" / "config.toml"
    codex_config_exists = codex_config_path.exists()
    if not codex_config_exists:
        files[codex_config_path] = CODEX_CONFIG

    result = write_files(
        files,
        root,
        args.force,
        protected_paths={
            agent_guidance_path,
            agent_notes_readme_path,
            reference_readme_path,
        },
    )
    if log_exists and (args.force or result["created"]):
        append_log_entry(
            log_path,
            root,
            project_name,
            ops_dir,
            args.force,
            result,
        )
    elif log_exists:
        result["skipped"].append(rel(log_path, root))
    result["ops_dir"] = rel(ops_dir, root)
    result["docs_dir"] = rel(docs_dir, root)
    result["name"] = project_name
    if agent_guidance_exists:
        result.setdefault("manual_merge", []).append(
            ".agents/AGENT-GUIDANCE.md already exists; preserved to avoid overwriting project-specific agent instructions."
        )
    if agent_notes_readme_exists:
        result.setdefault("manual_merge", []).append(
            ".agents/notes/README.md already exists; preserved to avoid overwriting project-specific agent notes guidance."
        )
    if reference_readme_exists:
        result.setdefault("manual_merge", []).append(
            "reference/README.md already exists; preserved to avoid overwriting project-specific reference guidance."
        )
    if agents_exists:
        result["skipped"].append("AGENTS.md")
        result.setdefault("manual_merge", []).extend([
            "AGENTS.md already exists; merge templates/AGENTS.md manually if needed.",
            ".agents/AGENT-GUIDANCE.md contains the reusable operating protocol unless it was also skipped.",
        ])
    if claude_settings_exists:
        result["skipped"].append(".claude/settings.json")
        result.setdefault("manual_merge", []).append(
            ".claude/settings.json already exists; preserved. To grant Claude Code maximum permissions, "
            'set "permissions": {"defaultMode": "bypassPermissions"} manually.'
        )
    if codex_config_exists:
        result["skipped"].append(".codex/config.toml")
        result.setdefault("manual_merge", []).append(
            ".codex/config.toml already exists; preserved. To grant Codex maximum permissions, set "
            'approval_policy = "never" and sandbox_mode = "danger-full-access" manually.'
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
