#!/usr/bin/env python3
"""Track B eval-harness skeleton (Stage 0 of the 10x roadmap).

The smallest honest measurement primitive: parse a rubric, parse a fixture, score
each criterion, weight-aggregate, compare to a threshold, and emit a verdict with a
non-zero exit on a regression. Spec: ``.agents/specs/eval-harness.md``.

The judge is pluggable. This slice ships a deterministic ``stub`` backend that
exercises the aggregation/threshold/verdict path reproducibly (it returns the
fixture's declared ``stub_scores``); the real LLM-as-judge backend lands in Stage 2
behind the same interface. ``build_judge_prompt`` already assembles the exact prompt a
real judge will receive.

Requires PyYAML (as ``validate_status.py`` does). When PyYAML is absent — a bare
``python3`` run without the CI dependency — ``--selftest`` skips with exit 0 so the
"just python3" local workflow is preserved.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# scripts/ -> assembly/ -> plugins/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
EVALS_DIR = REPO_ROOT / ".agents" / "evals"
RUBRICS_DIR = EVALS_DIR / "rubrics"
FIXTURES_DIR = EVALS_DIR / "fixtures"

SCORE_MIN, SCORE_MAX = 1, 5


class EvalError(Exception):
    """A structural problem with a rubric or fixture."""


def split_frontmatter(text: str, *, what: str) -> tuple[str, str]:
    """Return (frontmatter, body) for a ``---`` fenced markdown file."""
    if not text.startswith("---"):
        raise EvalError(f"{what}: missing YAML frontmatter (file must start with ---)")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise EvalError(f"{what}: unterminated YAML frontmatter")
    return parts[1], parts[2]


def load_rubric(rubric_id: str, rubrics_dir: Path) -> dict:
    import yaml

    path = rubrics_dir / f"{rubric_id}.md"
    if not path.is_file():
        raise EvalError(f"rubric not found: {path}")
    frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"), what=str(path))
    data = yaml.safe_load(frontmatter) or {}
    for key in ("id", "criteria", "threshold"):
        if key not in data:
            raise EvalError(f"{path}: rubric missing key: {key}")
    if not isinstance(data["criteria"], list) or not data["criteria"]:
        raise EvalError(f"{path}: criteria must be a non-empty list")
    for crit in data["criteria"]:
        for key in ("id", "weight"):
            if key not in crit:
                raise EvalError(f"{path}: criterion missing key: {key}")
    data["_anchors"] = body.strip()
    return data


def load_fixture(path: Path) -> tuple[dict, str]:
    import yaml

    frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"), what=str(path))
    data = yaml.safe_load(frontmatter) or {}
    for key in ("id", "rubric", "expect"):
        if key not in data:
            raise EvalError(f"{path}: fixture missing key: {key}")
    if data["expect"] not in ("pass", "fail"):
        raise EvalError(f"{path}: expect must be 'pass' or 'fail', got {data['expect']!r}")
    return data, body.strip()


def build_judge_prompt(rubric: dict, fixture: dict, candidate: str) -> str:
    """Assemble the prompt a real LLM judge receives. Backend-independent."""
    lines = [
        f"You are grading output for the `{rubric.get('area', '?')}` skill against a rubric.",
        "Score each criterion from 1 (worst) to 5 (best) using the anchors, then return per-criterion scores.",
        "",
        "## Criteria",
    ]
    for crit in rubric["criteria"]:
        lines.append(f"- {crit['id']} (weight {crit['weight']}): {crit.get('description', '')}")
    lines += ["", "## Anchors", rubric["_anchors"], "", "## Candidate output", candidate]
    return "\n".join(lines)


def judge_stub(rubric: dict, fixture: dict) -> dict:
    """Deterministic plumbing backend: return the fixture's declared scores."""
    scores = fixture.get("stub_scores")
    if not isinstance(scores, dict):
        raise EvalError(f"fixture {fixture['id']}: stub backend needs a stub_scores mapping")
    result = {}
    for crit in rubric["criteria"]:
        cid = crit["id"]
        if cid not in scores:
            raise EvalError(f"fixture {fixture['id']}: stub_scores missing criterion '{cid}'")
        value = scores[cid]
        if not isinstance(value, int) or not (SCORE_MIN <= value <= SCORE_MAX):
            raise EvalError(
                f"fixture {fixture['id']}: score for '{cid}' must be an int in "
                f"[{SCORE_MIN},{SCORE_MAX}], got {value!r}"
            )
        result[cid] = value
    return result


def judge_llm(rubric: dict, fixture: dict) -> dict:
    raise NotImplementedError(
        "the LLM judge backend lands in Stage 2 of the 10x roadmap; "
        "this skeleton ships the --judge stub backend only"
    )


JUDGES = {"stub": judge_stub, "llm": judge_llm}


def aggregate(rubric: dict, scores: dict) -> float:
    total_weight = sum(c["weight"] for c in rubric["criteria"])
    if total_weight <= 0:
        raise EvalError(f"rubric {rubric['id']}: criterion weights sum to zero")
    weighted = sum(scores[c["id"]] * c["weight"] for c in rubric["criteria"])
    return weighted / total_weight


def grade(fixture_path: Path, judge: str, rubrics_dir: Path) -> dict:
    fixture, candidate = load_fixture(fixture_path)
    rubric = load_rubric(fixture["rubric"], rubrics_dir)
    build_judge_prompt(rubric, fixture, candidate)  # assemble (and validate) the prompt
    scores = JUDGES[judge](rubric, fixture)
    score = aggregate(rubric, scores)
    verdict = "pass" if score >= rubric["threshold"] else "fail"
    return {
        "fixture": fixture["id"],
        "rubric": rubric["id"],
        "scores": scores,
        "aggregate": round(score, 3),
        "threshold": rubric["threshold"],
        "verdict": verdict,
        "expect": fixture["expect"],
    }


def print_result(r: dict) -> None:
    print(f"fixture: {r['fixture']}  rubric: {r['rubric']}")
    for cid, value in r["scores"].items():
        print(f"  {cid}: {value}")
    print(f"  aggregate {r['aggregate']} vs threshold {r['threshold']} -> {r['verdict'].upper()}")


def run_one(fixture_path: Path, judge: str, rubrics_dir: Path) -> int:
    result = grade(fixture_path, judge, rubrics_dir)
    print_result(result)
    return 0 if result["verdict"] == "pass" else 1


def run_selftest(rubrics_dir: Path, fixtures_dir: Path) -> int:
    fixtures = sorted(fixtures_dir.glob("*.md"))
    if not fixtures:
        print(f"FAIL: no fixtures found in {fixtures_dir}", file=sys.stderr)
        return 1
    failures = []
    for path in fixtures:
        result = grade(path, "stub", rubrics_dir)
        ok = result["verdict"] == result["expect"]
        # The judge prompt must mention every criterion — proves prompt assembly works.
        fixture, candidate = load_fixture(path)
        rubric = load_rubric(fixture["rubric"], rubrics_dir)
        prompt = build_judge_prompt(rubric, fixture, candidate)
        prompt_ok = all(c["id"] in prompt for c in rubric["criteria"])
        status = "ok" if (ok and prompt_ok) else "FAIL"
        print(
            f"[{status}] {result['fixture']}: verdict={result['verdict']} "
            f"expect={result['expect']} aggregate={result['aggregate']}"
        )
        if not ok:
            failures.append(f"{result['fixture']}: verdict {result['verdict']} != expect {result['expect']}")
        if not prompt_ok:
            failures.append(f"{result['fixture']}: judge prompt missing a criterion")
    if failures:
        print("FAIL: " + "; ".join(failures), file=sys.stderr)
        return 1
    print(f"OK: {len(fixtures)} fixtures scored end to end; all verdicts match expect")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track B eval-harness skeleton")
    parser.add_argument("--fixture", type=Path, help="grade a single fixture file")
    parser.add_argument("--judge", choices=sorted(JUDGES), default="stub")
    parser.add_argument("--rubrics-dir", type=Path, default=RUBRICS_DIR)
    parser.add_argument("--fixtures-dir", type=Path, default=FIXTURES_DIR)
    parser.add_argument("--selftest", action="store_true", help="run all fixtures with the stub judge")
    args = parser.parse_args(argv)

    try:
        import yaml  # noqa: F401
    except ModuleNotFoundError:
        print("SKIP: PyYAML not installed; eval harness not run (CI installs it).")
        return 0

    try:
        if args.selftest:
            return run_selftest(args.rubrics_dir, args.fixtures_dir)
        if args.fixture:
            return run_one(args.fixture, args.judge, args.rubrics_dir)
    except (EvalError, NotImplementedError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    parser.print_usage()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
