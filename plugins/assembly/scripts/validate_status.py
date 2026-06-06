#!/usr/bin/env python3
"""Validate the machine-readable status block in docs/status.md.

Stage 0 of the 10x roadmap makes project state machine-readable so tools, CI,
and external operators can read it instead of re-parsing prose. This validator
keeps that block honest: it must parse, carry the required shape, use known
enum values, and point only at verification commands whose scripts exist.

Requires PyYAML. When PyYAML is absent (a bare ``python3`` run without the CI
dependency installed), it skips with a clear message and exit 0, so the
"just python3" local workflow is preserved.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


# scripts/ -> assembly/ -> plugins/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
STATUS_FILE = REPO_ROOT / "docs" / "status.md"

SCHEMA = "assembly-status/v1"
REQUIRED_TOP_LEVEL = {
    "schema",
    "project",
    "phase",
    "current_gate",
    "next_skill",
    "traffic_state",
    "blocked",
    "needs_founder_input",
    "last_verified",
    "autonomy",
    "verification",
    "escalation_floor",
}
REQUIRED_AUTONOMY = {"product_decisions", "engineering_decisions", "merge", "deploy"}
TRAFFIC_STATES = {"pre-live", "live"}


class StatusError(Exception):
    """A structural problem with the status block."""


def extract_block(text: str) -> str:
    """Return the YAML fenced block that carries the status schema."""
    blocks = re.findall(r"```yaml\n(.*?)```", text, flags=re.DOTALL)
    for block in blocks:
        if f"schema: {SCHEMA}" in block:
            return block
    raise StatusError(
        f"no ```yaml block with `schema: {SCHEMA}` found in docs/status.md"
    )


def validate(data: dict) -> None:
    if not isinstance(data, dict):
        raise StatusError("status block is not a mapping")

    missing = sorted(REQUIRED_TOP_LEVEL - data.keys())
    if missing:
        raise StatusError(f"missing required keys: {', '.join(missing)}")

    if data["schema"] != SCHEMA:
        raise StatusError(f"schema must be {SCHEMA!r}, got {data['schema']!r}")

    if data["traffic_state"] not in TRAFFIC_STATES:
        raise StatusError(
            f"traffic_state must be one of {sorted(TRAFFIC_STATES)}, "
            f"got {data['traffic_state']!r}"
        )

    for key in ("blocked", "needs_founder_input"):
        if not isinstance(data[key], bool):
            raise StatusError(f"{key} must be a boolean, got {data[key]!r}")

    autonomy = data["autonomy"]
    if not isinstance(autonomy, dict):
        raise StatusError("autonomy must be a mapping")
    missing_autonomy = sorted(REQUIRED_AUTONOMY - autonomy.keys())
    if missing_autonomy:
        raise StatusError(f"autonomy missing keys: {', '.join(missing_autonomy)}")

    verification = data["verification"]
    if not isinstance(verification, dict):
        raise StatusError("verification must be a mapping")
    for key in ("ci", "validators"):
        if key not in verification:
            raise StatusError(f"verification missing key: {key}")

    ci_path = REPO_ROOT / verification["ci"]
    if not ci_path.is_file():
        raise StatusError(f"verification.ci points at a missing file: {verification['ci']}")

    validators = verification["validators"]
    if not isinstance(validators, list) or not validators:
        raise StatusError("verification.validators must be a non-empty list")
    for cmd in validators:
        # Each command references a script path as a bare token; the referenced
        # file must exist so the block cannot drift away from reality.
        script = next(
            (tok for tok in cmd.split() if tok.endswith(".py")),
            None,
        )
        if script is None:
            raise StatusError(f"validator command names no .py script: {cmd!r}")
        if not (REPO_ROOT / script).is_file():
            raise StatusError(f"validator references a missing script: {script}")

    escalation = data["escalation_floor"]
    if not isinstance(escalation, list) or not escalation:
        raise StatusError("escalation_floor must be a non-empty list")

    # capabilities is optional (added by the capability-acquisition behavior), but
    # when present it must carry the durable shape the AGENTS.md mirror relies on.
    capabilities = data.get("capabilities")
    if capabilities is not None:
        if not isinstance(capabilities, list):
            raise StatusError("capabilities must be a list when present")
        for index, entry in enumerate(capabilities):
            if not isinstance(entry, dict):
                raise StatusError(f"capabilities[{index}] must be a mapping")
            for key in ("name", "source"):
                if key not in entry:
                    raise StatusError(f"capabilities[{index}] missing key: {key}")


def main() -> int:
    try:
        import yaml
    except ModuleNotFoundError:
        print("SKIP: PyYAML not installed; status block not validated (CI installs it).")
        return 0

    if not STATUS_FILE.is_file():
        print(f"FAIL: {STATUS_FILE} not found", file=sys.stderr)
        return 1

    try:
        block = extract_block(STATUS_FILE.read_text(encoding="utf-8"))
        data = yaml.safe_load(block)
        validate(data)
    except StatusError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except yaml.YAMLError as exc:
        print(f"FAIL: status block is not valid YAML: {exc}", file=sys.stderr)
        return 1

    print("OK: machine-readable status block is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
