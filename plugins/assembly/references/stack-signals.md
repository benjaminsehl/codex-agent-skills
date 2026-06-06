# Stack Detection Signals

`scripts/detect_stack.py` infers a project's stack from repo signals so the
capability-acquisition behavior (see `.agents/specs/capability-assembly.md`) can
search skills.sh for the right domain skills. This file documents the seed signal
set and how to extend it. The script's `STACK_SIGNALS` table is the source of
truth; keep this doc in sync when you add a stack.

## How detection works

- The script inspects a repo root for **marker files** and **package.json
  dependencies** (across `dependencies`, `devDependencies`, `peerDependencies`,
  and `optionalDependencies`).
- A dependency pattern ending in `/` matches by prefix (scoped packages like
  `@cloudflare/...`); otherwise it matches the dependency name exactly.
- Detection is **multi-stack**: every stack whose signals match is reported (e.g.
  a Next.js app deployed on Cloudflare reports both).
- `node` is a **fallback**: reported only when a `package.json` exists and no more
  specific framework matched, so it never adds noise next to a real framework.
- Output is JSON: `{root, stacks, signals}`, where `signals` maps each detected
  stack to the concrete markers that matched.

## Seed signal set

| Stack | Marker files | Dependency patterns |
| --- | --- | --- |
| `cloudflare` | `wrangler.toml`, `wrangler.jsonc`, `wrangler.json` | `wrangler`, `@cloudflare/` |
| `nextjs` | `next.config.{js,mjs,cjs,ts}` | `next` |
| `remix` | `remix.config.js` | `@remix-run/` |
| `astro` | `astro.config.{mjs,ts,js}` | `astro` |
| `sveltekit` | `svelte.config.js` | `@sveltejs/kit` |
| `vite` | `vite.config.{js,ts,mjs}` | `vite` |
| `vercel` | `vercel.json` | — |
| `node` (fallback) | `package.json` (only if nothing more specific matched) | — |

## Extending

1. Add an entry to `STACK_SIGNALS` in `scripts/detect_stack.py` (marker files and
   dependency patterns).
2. Add a row to the table above.
3. Add a `--selftest` case in `detect_stack.py` proving the new stack detects.

Keep the set small and high-signal — it should grow from real projects, not
speculation. Stack detection only observes; the founder still confirms the
inferred stack before any search or install.

## Usage

```bash
python3 plugins/assembly/scripts/detect_stack.py --root /path/to/repo
python3 plugins/assembly/scripts/detect_stack.py --selftest   # fixture tests
```
