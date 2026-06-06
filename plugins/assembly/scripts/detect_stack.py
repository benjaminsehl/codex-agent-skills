#!/usr/bin/env python3
"""Detect a project's stack from repo signals.

Capability assembly (see docs/specs/capability-assembly.md) needs to know a
project's stack before it can search skills.sh for the right domain skills. This
script is the deterministic, testable seam: given a repo root, it reports the
stack(s) it can infer and the concrete signals that matched, as JSON. The
interactive "confirm before searching" step lives in the capability-acquisition
behavior, not here — this script only observes.

The signal table below is the seed set; it is documented for humans in
``plugins/assembly/references/stack-signals.md`` and is meant to grow from use.
Keep the two in sync when adding a stack.

stdlib-only by design, so the "just python3" workflow and CI both run it without
extra dependencies. ``--selftest`` exercises the detector against temporary
fixtures and is run in CI.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path


# Each stack lists the marker files and package.json dependency patterns that
# signal it. A dependency pattern ending in "/" matches by prefix (scoped
# packages like "@cloudflare/..."); otherwise it matches the dependency name
# exactly. "node" is a deliberate fallback: it only reports when a package.json
# exists and no more specific framework matched, so it never adds noise next to
# a real framework.
STACK_SIGNALS: dict[str, dict[str, list[str]]] = {
    "cloudflare": {
        "files": ["wrangler.toml", "wrangler.jsonc", "wrangler.json"],
        "deps": ["wrangler", "@cloudflare/"],
    },
    "nextjs": {
        "files": ["next.config.js", "next.config.mjs", "next.config.cjs", "next.config.ts"],
        "deps": ["next"],
    },
    "remix": {
        "files": ["remix.config.js"],
        "deps": ["@remix-run/"],
    },
    "astro": {
        "files": ["astro.config.mjs", "astro.config.ts", "astro.config.js"],
        "deps": ["astro"],
    },
    "sveltekit": {
        "files": ["svelte.config.js"],
        "deps": ["@sveltejs/kit"],
    },
    "vite": {
        "files": ["vite.config.js", "vite.config.ts", "vite.config.mjs"],
        "deps": ["vite"],
    },
    "vercel": {
        "files": ["vercel.json"],
        "deps": [],
    },
}

# Reported only when a package.json exists and nothing more specific matched.
FALLBACK_STACK = "node"


def _read_package_dependencies(root: Path) -> set[str]:
    """Return the union of dependency names across package.json dep sections."""
    pkg = root / "package.json"
    if not pkg.is_file():
        return set()
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()
    names: set[str] = set()
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        block = data.get(section)
        if isinstance(block, dict):
            names.update(block.keys())
    return names


def _dep_matches(pattern: str, deps: set[str]) -> str | None:
    """Return the matching dependency name, or None."""
    if pattern.endswith("/"):
        for dep in sorted(deps):
            if dep.startswith(pattern):
                return dep
        return None
    return pattern if pattern in deps else None


def detect(root: Path) -> dict:
    """Detect stacks under ``root``. Returns {root, stacks, signals}."""
    deps = _read_package_dependencies(root)
    signals: dict[str, list[str]] = {}

    for stack, markers in STACK_SIGNALS.items():
        matched: list[str] = []
        for filename in markers["files"]:
            if (root / filename).is_file():
                matched.append(filename)
        for pattern in markers["deps"]:
            dep = _dep_matches(pattern, deps)
            if dep is not None:
                matched.append(f"dependency:{dep}")
        if matched:
            signals[stack] = matched

    if not signals and (root / "package.json").is_file():
        signals[FALLBACK_STACK] = ["package.json"]

    return {
        "root": str(root),
        "stacks": sorted(signals.keys()),
        "signals": {stack: signals[stack] for stack in sorted(signals.keys())},
    }


def _selftest() -> int:
    """Exercise the detector against temporary fixtures."""
    cases: list[tuple[str, dict[str, str], list[str]]] = [
        ("cloudflare via wrangler.toml", {"wrangler.toml": "name = 'x'\n"}, ["cloudflare"]),
        (
            "nextjs via config + dep",
            {"next.config.js": "module.exports = {}\n", "package.json": '{"dependencies":{"next":"14"}}'},
            ["nextjs"],
        ),
        (
            "multi-stack: next on cloudflare",
            {
                "wrangler.toml": "name = 'x'\n",
                "next.config.js": "module.exports = {}\n",
                "package.json": '{"dependencies":{"next":"14"}}',
            },
            ["cloudflare", "nextjs"],
        ),
        ("scoped dep: sveltekit", {"package.json": '{"devDependencies":{"@sveltejs/kit":"2"}}'}, ["sveltekit"]),
        ("node fallback", {"package.json": '{"name":"plain"}'}, ["node"]),
        ("empty repo", {}, []),
    ]
    failures = 0
    for label, files, expected in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, content in files.items():
                (root / name).write_text(content, encoding="utf-8")
            got = detect(root)["stacks"]
            if got != expected:
                failures += 1
                print(f"FAIL: {label}: expected {expected}, got {got}", file=sys.stderr)
            else:
                print(f"OK: {label} -> {got}")
    if failures:
        print(f"FAIL: {failures} selftest case(s) failed", file=sys.stderr)
        return 1
    print("OK: detect_stack selftest passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect a project's stack from repo signals.")
    parser.add_argument("--root", default=".", help="Repo root to inspect (default: current directory).")
    parser.add_argument("--selftest", action="store_true", help="Run built-in fixture tests and exit.")
    args = parser.parse_args(argv)

    if args.selftest:
        return _selftest()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"FAIL: --root is not a directory: {root}", file=sys.stderr)
        return 1

    print(json.dumps(detect(root), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
