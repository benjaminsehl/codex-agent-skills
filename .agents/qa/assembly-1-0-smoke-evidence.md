# QA Evidence: Assembly 1.0 Smoke Tests

Last updated: 2026-05-27
Status: partial evidence captured

## Scope

Record evidence for Assembly 1.0 release readiness.

## Automated Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `python3 plugins/assembly/scripts/validate_plugin.py` | Pass | `OK: plugin shape is valid` |
| `python3 plugins/assembly/scripts/validate_skill_graph.py` | Pass | `OK: skill references are valid` |
| `python3 plugins/assembly/scripts/audit_skill_conflicts.py` | Pass | No public-skill conflicts in active local skill roots |
| `python3 -m py_compile ...` | Pass | No output |
| `git diff --check` | Pass | No output |

## Behavior Prompts

Run each prompt in both Codex and Claude Code. Record results in separate columns so dual-runtime parity is visible.

| Prompt | Codex Result | Claude Code Result | Notes |
| --- | --- | --- | --- |
| `Use next to do the next normal thing.` | Not run | Not run | Must name phase, evidence, next skill, and status update behavior. |
| `Use project-status to tell me what phase this project is in.` | Not run | Not run | Must cite files and missing prerequisites. |
| `Use product-discovery on this idea.` | Not run | Not run | Must interview before deciding. |
| `Use product-discovery and make the calls for this idea.` | Not run | Not run | Must label assumptions and recommendations. |
| `Use build.` | Not run | Not run | Must infer first unambiguous build-track gate or ask if ambiguous. |
| `Use build, then push this up.` | Not run | Not run | Must produce or update a descriptive draft PR when material changes exist. |
| `Use qa on this local app.` | Not run | Not run | Must test like a user and report repro steps for bugs. |
| `Use ship to decide whether this is ready.` | Not run | Not run | Must produce GO/NO-GO with blockers, risks, evidence, and rollback. |

## Install Checks

| Check | Codex Result | Claude Code Result | Evidence |
| --- | --- | --- | --- |
| Public marketplace add | Not run | Not run | Pending release-candidate pass |
| Marketplace upgrade | Not run | Not run | Pending release-candidate pass |
| Fresh session sees Assembly | Not run | Not run | Pending release-candidate pass |
| Composer icon renders | Not run | Not run | Pending release-candidate pass |

## Proof Projects

| Project | Required | Result | Evidence |
| --- | --- | --- | --- |
| Assembly | Yes | In progress | This branch is the self-host spec gate. |
| CFO | Yes | Not run | Pending explicit proof pass. |
| Hyper | Stretch | Deferred | Useful retrofit proof, not blocking for 1.0. |

## Release Notes

Behavior prompts, install checks, CFO proof, and release checks still need to be run during the release-candidate pass. Do not mark 1.0 ready from automated validation alone.
