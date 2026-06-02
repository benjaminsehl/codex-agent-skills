#!/usr/bin/env python3
"""Validate the Assembly plugin shape."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = (
    PLUGIN_ROOT.parents[1]
    if PLUGIN_ROOT.parent.name == "plugins"
    else PLUGIN_ROOT
)
PLUGIN_NAME = PLUGIN_ROOT.name
PUBLIC_SKILLS = {
    "next",
    "init",
    "spec",
    "plan",
    "build",
    "test",
    "review",
    "code-simplify",
    "ship",
    "product-discovery",
    "qa",
    "prototype",
    "project-status",
}
REQUIRED_REFERENCES = {
    "accessibility-checklist.md",
    "performance-checklist.md",
    "security-checklist.md",
    "testing-patterns.md",
    "product-discovery-checklist.md",
    "business-model-checklist.md",
    "design-quality-checklist.md",
    "qa-checklist.md",
    "project-phases.md",
    "project-kernel-structure.md",
    "matt-pocock-skills-notes.md",
    "hyper-project-notes.md",
    "agent-operating-protocol.md",
    "workflows/project-lifecycle.md",
    "workflows/product-strategy.md",
    "workflows/engineering-delivery.md",
    "workflows/qa-and-release.md",
}
REQUIRED_PERSONAS = {
    "code-reviewer.md",
    "security-auditor.md",
    "test-engineer.md",
}


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing required file: {rel(path)}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {rel(path)}: {exc}")


def rel(path: Path) -> str:
    for root in (PLUGIN_ROOT, REPO_ROOT):
        try:
            return str(path.relative_to(root))
        except ValueError:
            continue
    return str(path)


def resolve_plugin_path(value: str) -> Path:
    if not value.startswith("./"):
        fail(f"Manifest path must be relative and start with ./, got {value!r}")
    return (PLUGIN_ROOT / value[2:]).resolve()


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{rel(path)} must start with YAML frontmatter")

    end = text.find("\n---", 4)
    if end == -1:
        fail(f"{rel(path)} is missing closing frontmatter marker")

    raw = text[4:end].strip()
    body = text[end + len("\n---") :].strip()
    metadata: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" ") or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, body


def validate_codex_manifest() -> None:
    manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    manifest = load_json(manifest_path)

    if manifest.get("name") != PLUGIN_NAME:
        fail("Codex manifest name must match the plugin folder name")
    if manifest.get("skills") != "./skills/":
        fail('Codex manifest must set "skills" to "./skills/"')
    if manifest.get("license") != "MIT":
        fail('Codex plugin manifest must set "license" to "MIT"')
    if not (PLUGIN_ROOT / "LICENSE").is_file():
        fail("Public plugin bundle must include a LICENSE file")

    skills_dir = resolve_plugin_path(manifest["skills"])
    if not skills_dir.is_dir():
        fail("Codex manifest skills path does not exist")

    for key in ("hooks", "mcpServers", "apps"):
        if key in manifest:
            target = resolve_plugin_path(str(manifest[key]))
            if not target.exists():
                fail(f"Codex manifest {key} path does not exist: {manifest[key]}")

    prompts = manifest.get("interface", {}).get("defaultPrompt", [])
    if len(prompts) > 3:
        fail("interface.defaultPrompt must contain at most 3 prompts")
    for prompt in prompts:
        if len(prompt) > 128:
            fail(f"interface.defaultPrompt entry is over 128 characters: {prompt!r}")


def validate_claude_manifest() -> None:
    manifest_path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    manifest = load_json(manifest_path)

    if manifest.get("name") != PLUGIN_NAME:
        fail("Claude Code manifest name must match the plugin folder name")
    if manifest.get("license") != "MIT":
        fail('Claude Code plugin manifest must set "license" to "MIT"')
    if not manifest.get("description"):
        fail("Claude Code manifest must include a description")
    if not manifest.get("version"):
        fail("Claude Code manifest must declare a version so updates are intentional")

    for key in ("skills", "commands", "agents"):
        value = manifest.get(key)
        if value is None:
            continue
        targets = value if isinstance(value, list) else [value]
        for target in targets:
            if not isinstance(target, str) or not target.startswith("./"):
                fail(
                    f"Claude Code manifest {key} entry must be a relative path starting with ./, got {target!r}"
                )
            if not resolve_plugin_path(target).exists():
                fail(f"Claude Code manifest {key} path does not exist: {target}")


def validate_codex_marketplace() -> None:
    path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
    marketplace = load_json(path)
    if marketplace.get("name") != PLUGIN_NAME:
        fail("Codex marketplace name must match the plugin name")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        fail("Codex marketplace must contain at least one plugin entry")

    matching = [entry for entry in entries if entry.get("name") == PLUGIN_NAME]
    if len(matching) != 1:
        fail(f"Codex marketplace must contain exactly one {PLUGIN_NAME} entry")

    entry = matching[0]
    if entry.get("source", {}).get("source") != "local":
        fail("Codex marketplace entry source must be local")
    expected_path = f"./plugins/{PLUGIN_NAME}"
    if entry.get("source", {}).get("path") != expected_path:
        fail(f'Codex marketplace entry source.path must be "{expected_path}"')
    if entry.get("policy", {}).get("installation") != "AVAILABLE":
        fail("Codex marketplace installation policy must be AVAILABLE")
    if entry.get("policy", {}).get("authentication") != "ON_INSTALL":
        fail("Codex marketplace authentication policy must be ON_INSTALL")
    if not entry.get("category"):
        fail("Codex marketplace entry must include a category")


def validate_claude_marketplace() -> None:
    path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = load_json(path)

    if marketplace.get("name") != PLUGIN_NAME:
        fail("Claude Code marketplace name must match the plugin name")

    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        fail("Claude Code marketplace must include owner.name")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        fail("Claude Code marketplace must contain at least one plugin entry")

    matching = [entry for entry in entries if entry.get("name") == PLUGIN_NAME]
    if len(matching) != 1:
        fail(f"Claude Code marketplace must contain exactly one {PLUGIN_NAME} entry")

    entry = matching[0]
    source = entry.get("source")
    expected_path = f"./plugins/{PLUGIN_NAME}"
    if source != expected_path:
        fail(
            f'Claude Code marketplace entry source must be the relative path "{expected_path}"'
        )
    if not entry.get("category"):
        fail("Claude Code marketplace entry must include a category")


def validate_skill(path: Path) -> None:
    metadata, body = parse_frontmatter(path)
    rel_path = rel(path)
    skill_dir = path.parent.name

    if metadata.get("name") != skill_dir:
        fail(f"{rel_path} frontmatter name must match directory name {skill_dir!r}")
    description = metadata.get("description", "")
    if not description or len(description) < 30:
        fail(f"{rel_path} must include a useful description")
    if len(description.split()) > 45:
        fail(f"{rel_path} description is too broad; keep trigger text concise")
    if "[TODO" in body or "[TODO" in description:
        fail(f"{rel_path} contains unresolved TODO placeholder text")
    if len(body.split()) < 25:
        fail(f"{rel_path} body is too short to be a useful workflow")

    for heading in ("## Purpose", "## References", "## Workflow", "## Verification"):
        if heading not in body:
            fail(f"{rel_path} public skill is missing {heading}")
    if "## Stop Conditions" not in body:
        fail(f"{rel_path} public skill is missing ## Stop Conditions")
    if "## Underlying skills" in body:
        fail(f"{rel_path} must use references, not triggerable underlying skills")
    if len(body.splitlines()) > 120:
        fail(f"{rel_path} is too large; keep public skills thin")


def validate_skills() -> None:
    skills_dir = PLUGIN_ROOT / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    names = {path.parent.name for path in skill_files}

    missing = sorted(PUBLIC_SKILLS - names)
    if missing:
        fail(f"Missing required skills: {', '.join(missing)}")

    unexpected = sorted(names - PUBLIC_SKILLS)
    if unexpected:
        fail(f"Unexpected triggerable skills: {', '.join(unexpected)}")

    for path in skill_files:
        validate_skill(path)

    duplicate_names = [
        name for name in names if len(list(skills_dir.glob(f"{re.escape(name)}/SKILL.md"))) > 1
    ]
    if duplicate_names:
        fail(f"Duplicate skill names found: {', '.join(sorted(duplicate_names))}")


def validate_support_files() -> None:
    references_dir = PLUGIN_ROOT / "references"
    missing_refs = sorted(name for name in REQUIRED_REFERENCES if not (references_dir / name).is_file())
    if missing_refs:
        fail(f"Missing required references: {', '.join(missing_refs)}")

    for path in sorted(references_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel_path = rel(path)
        if len(text.splitlines()) > 100 and "## Contents" not in text and "## Table of Contents" not in text:
            fail(f"{rel_path} is over 100 lines and must include a ## Contents section")

    install_text = (PLUGIN_ROOT / "docs" / "INSTALL.md").read_text(encoding="utf-8")
    for required in (
        "Existing Skill Conflicts",
        "Replacing A Loose Skill Set",
        "disable",
        "rename",
        "entry skills",
        "next",
        "spec",
        "plan",
        "build",
        "test",
        "review",
        "ship",
    ):
        if required not in install_text:
            fail(f"docs/INSTALL.md must document skill-conflict guidance: {required}")
    for required in (
        "Claude Code",
        "Codex",
        "/plugin marketplace add benjaminsehl/assembly",
        "codex plugin marketplace add benjaminsehl/assembly",
    ):
        if required not in install_text:
            fail(
                f"docs/INSTALL.md must document dual-runtime install path: {required}"
            )

    readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    if "de-duplicate" not in readme_text or "lifecycle" not in readme_text:
        fail("README.md must include lifecycle de-duplication guidance")
    for required in (
        "Claude Code",
        "Codex",
        "/plugin marketplace add benjaminsehl/assembly",
        "codex plugin marketplace add benjaminsehl/assembly",
    ):
        if required not in readme_text:
            fail(
                f"README.md must document dual-runtime install path: {required}"
            )
    for required in (
        "Autonomy Model",
        "traffic state",
        "pre-live",
        "reviewer sub-agents",
    ):
        if required not in readme_text:
            fail(
                f"README.md must document the traffic-state autonomy model: {required}"
            )
    for required in (
        "always-ask floor",
        "review threads",
        "product-implication language",
    ):
        if required not in readme_text:
            fail(f"README.md must document the escalation model: {required}")

    command_contract_text = (PLUGIN_ROOT / "docs" / "COMMAND_CONTRACT.md").read_text(encoding="utf-8")
    for required in (
        "traffic state",
        "PR review feedback",
        "reviewer sub-agents",
    ):
        if required not in command_contract_text:
            fail(f"docs/COMMAND_CONTRACT.md must document GitHub handoff behavior: {required}")

    template_text = (PLUGIN_ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")
    if "Assembly" not in template_text or "lifecycle" not in template_text:
        fail("templates/AGENTS.md must identify Assembly as lifecycle owner")
    if ".agents/AGENT-GUIDANCE.md" not in template_text:
        fail("templates/AGENTS.md must point to .agents/AGENT-GUIDANCE.md")

    project_structure_text = (PLUGIN_ROOT / "references" / "project-kernel-structure.md").read_text(encoding="utf-8")
    for required in (
        ".agents/AGENT-GUIDANCE.md",
        ".agents/log.md",
        ".agents/notes/",
        "reference/",
        "append-only",
        "protected once they exist",
        ".agents/notes/README.md",
        "reference/README.md",
        ".claude/settings.json",
        ".codex/config.toml",
        "bypassPermissions",
        "danger-full-access",
    ):
        if required not in project_structure_text:
            fail(f"project-kernel-structure.md must document scaffold path: {required}")

    agents_dir = PLUGIN_ROOT / ".agents" / "personas"
    if not (agents_dir / "README.md").is_file():
        fail("Missing required persona docs: .agents/personas/README.md")
    missing_personas = sorted(
        name for name in REQUIRED_PERSONAS if not (agents_dir / name).is_file()
    )
    if missing_personas:
        fail(f"Missing required personas: {', '.join(missing_personas)}")

    scaffold_script = PLUGIN_ROOT / "scripts" / "scaffold_project.py"
    if not scaffold_script.is_file():
        fail("Missing required scaffold script: scripts/scaffold_project.py")
    validate_scaffold_behavior(scaffold_script)

    engineering_text = (
        PLUGIN_ROOT / "references" / "workflows" / "engineering-delivery.md"
    ).read_text(encoding="utf-8")
    for required in (
        "git switch <topic-branch> || git switch -c <topic-branch>",
        "Build is a router",
        "characterization tests",
        "mini-discovery",
        "Fan out specialist",
    ):
        if required not in engineering_text:
            fail(f"engineering-delivery.md must encode the locked skill behaviors: {required}")

    spec_text = (PLUGIN_ROOT / "skills" / "spec" / "SKILL.md").read_text(encoding="utf-8")
    if "mini-discovery" not in spec_text:
        fail("spec skill must document mini-discovery requirement")

    build_text = (PLUGIN_ROOT / "skills" / "build" / "SKILL.md").read_text(encoding="utf-8")
    for required in ("router, not a dispatcher", "What Build Does Not Do"):
        if required not in build_text:
            fail(f"build skill must encode router model: {required}")

    test_text = (PLUGIN_ROOT / "skills" / "test" / "SKILL.md").read_text(encoding="utf-8")
    if "characterization tests" not in test_text:
        fail("test skill must require characterization tests for legacy code")

    review_text = (PLUGIN_ROOT / "skills" / "review" / "SKILL.md").read_text(encoding="utf-8")
    if "Fan out specialist" not in review_text:
        fail("review skill must use parallel specialist fan-out")

    ship_text = (PLUGIN_ROOT / "skills" / "ship" / "SKILL.md").read_text(encoding="utf-8")
    for required in ("handoff is blocked", "binary", "GO", "NO-GO"):
        if required not in ship_text:
            fail(f"ship skill must encode binary release decision and blocked handoff: {required}")

    next_text = (PLUGIN_ROOT / "skills" / "next" / "SKILL.md").read_text(encoding="utf-8")
    for required in (
        "references/workflows/qa-and-release.md",
        "product gates",
        "always-ask floor",
        "product-implication language",
        "traffic state",
        "reviewer sub-agents",
        "What is being built",
        "Why it matters",
        "What good looks like",
        "Rollback",
        "2-3",
        "scaffold the project",
    ):
        if required not in next_text:
            fail(f"next skill must encode the gating model and founder calls: {required}")

    product_discovery_text = (
        PLUGIN_ROOT / "skills" / "product-discovery" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for required in (
        "founder/product director",
        "what is being built",
        "why it matters",
        "what good looks like",
        "product-implication language",
        "Flag business, user, and viability concerns",
        "docs/product/discovery-",
        "risk-triggered",
    ):
        if required not in product_discovery_text:
            fail(f"product-discovery must document interview-first founder behavior: {required}")

    project_status_text = (
        PLUGIN_ROOT / "skills" / "project-status" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for required in ("tech design", "research", "what is being built", "why it matters", "what good looks like"):
        if required not in project_status_text:
            fail(f"project-status must inspect core project context: {required}")

    qa_release_text = (
        PLUGIN_ROOT / "references" / "workflows" / "qa-and-release.md"
    ).read_text(encoding="utf-8")
    for required in (
        "reviewer sub-agents",
        "pre-live",
        "PR Review Feedback",
        "GitHub Handoff",
        "gh pr edit",
        "handoff is blocked",
        "binary",
        "traffic state",
    ):
        if required not in qa_release_text:
            fail(f"qa-and-release.md must encode ship-owned handoff and locked decisions: {required}")

    if not (PLUGIN_ROOT / "AGENTS.md").is_file():
        fail("Missing required plugin agent guidance: AGENTS.md")
    if not (PLUGIN_ROOT / "templates" / "AGENTS.md").is_file():
        fail("Missing required downstream agent template: templates/AGENTS.md")


def run_scaffold(scaffold_script: Path, root: Path, *args: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(scaffold_script), "--root", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        fail(f"scaffold_project.py returned invalid JSON: {exc}")


def reported_paths(result: dict, key: str) -> set[str]:
    return {str(value).replace("\\", "/") for value in result.get(key, [])}


def validate_scaffold_behavior(scaffold_script: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="assembly-scaffold-") as temp_dir:
        root = Path(temp_dir) / "project"
        root.mkdir()

        result = run_scaffold(scaffold_script, root, "--name", "Root Project")
        for required in (
            "AGENTS.md",
            ".agents/AGENT-GUIDANCE.md",
            ".agents/log.md",
            ".agents/notes/README.md",
            "reference/README.md",
            ".agents/status.md",
            ".claude/settings.json",
            ".codex/config.toml",
        ):
            if not (root / required).is_file():
                fail(f"scaffold_project.py did not create {required}")
            if required not in reported_paths(result, "created"):
                fail(f"scaffold_project.py did not report created file {required}")
        if (root / "docs" / "agent-guidance.md").exists():
            fail("scaffold_project.py created deprecated docs/agent-guidance.md")

        claude_settings = json.loads(
            (root / ".claude" / "settings.json").read_text(encoding="utf-8")
        )
        if claude_settings.get("permissions", {}).get("defaultMode") != "bypassPermissions":
            fail("scaffold_project.py must grant Claude Code bypassPermissions by default")
        codex_config = (root / ".codex" / "config.toml").read_text(encoding="utf-8")
        if 'approval_policy = "never"' not in codex_config or 'sandbox_mode = "danger-full-access"' not in codex_config:
            fail("scaffold_project.py must grant Codex maximum permissions by default")

        (root / ".agents" / "AGENT-GUIDANCE.md").write_text(
            "# Custom Guidance\n\nKeep me.\n", encoding="utf-8"
        )
        (root / ".agents" / "notes" / "README.md").write_text(
            "# Custom Notes Readme\n\nKeep notes.\n", encoding="utf-8"
        )
        (root / "reference" / "README.md").write_text(
            "# Custom Reference Readme\n\nKeep reference.\n", encoding="utf-8"
        )
        (root / ".agents" / "log.md").write_text(
            "# Agent Log\n\nCUSTOM LOG LINE\n", encoding="utf-8"
        )
        (root / ".claude" / "settings.json").write_text(
            '{"permissions": {"defaultMode": "default"}, "custom": "keep"}\n',
            encoding="utf-8",
        )
        (root / ".codex" / "config.toml").write_text(
            "# CUSTOM CODEX CONFIG\napproval_policy = \"untrusted\"\n", encoding="utf-8"
        )

        forced = run_scaffold(
            scaffold_script,
            root,
            "--name",
            "Child Project",
            "--slug",
            "child",
            "--force",
        )
        preserved = {
            ".agents/AGENT-GUIDANCE.md": "Keep me.",
            ".agents/notes/README.md": "Keep notes.",
            "reference/README.md": "Keep reference.",
        }
        for path, marker in preserved.items():
            if marker not in (root / path).read_text(encoding="utf-8"):
                fail(f"force scaffold overwrote protected file {path}")
            if path not in reported_paths(forced, "skipped"):
                fail(f"force scaffold did not report protected skip for {path}")
        for path, marker in (
            (".claude/settings.json", '"custom": "keep"'),
            (".codex/config.toml", "CUSTOM CODEX CONFIG"),
        ):
            if marker not in (root / path).read_text(encoding="utf-8"):
                fail(f"force scaffold overwrote existing permission config {path}")
            if path not in reported_paths(forced, "skipped"):
                fail(f"force scaffold did not report preserved permission config {path}")

        log_text = (root / ".agents" / "log.md").read_text(encoding="utf-8")
        if "CUSTOM LOG LINE" not in log_text or "force-refreshed" not in log_text:
            fail("force scaffold did not append to .agents/log.md")
        if ".agents/log.md" not in reported_paths(forced, "updated"):
            fail("force scaffold did not report .agents/log.md as updated")
        if not (root / ".agents" / "projects" / "child" / "status.md").is_file():
            fail("force scaffold did not create child project operational status.md")
        if not (root / "docs" / "projects" / "child" / "README.md").is_file():
            fail("force scaffold did not create child project human README.md")

        log_dir_root = Path(temp_dir) / "log-dir-project"
        (log_dir_root / ".agents" / "log.md").mkdir(parents=True)
        log_dir_result = run_scaffold(scaffold_script, log_dir_root, "--name", "Log Dir")
        if not (log_dir_root / ".agents" / "log.md").is_dir():
            fail("scaffold_project.py overwrote non-file .agents/log.md path")
        if ".agents/log.md" not in reported_paths(log_dir_result, "skipped"):
            fail("scaffold_project.py did not report non-file .agents/log.md as skipped")


def main() -> int:
    checks = (
        validate_codex_manifest,
        validate_claude_manifest,
        validate_codex_marketplace,
        validate_claude_marketplace,
        validate_skills,
        validate_support_files,
    )
    try:
        for check in checks:
            check()
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("OK: plugin shape is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
