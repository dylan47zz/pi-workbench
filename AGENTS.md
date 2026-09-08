# Pi Workbench — Agent Context

Pi Workbench is a personal operating layer over an Obsidian-compatible Vault. Its canonical lifecycle is:

```text
raw/ -> wiki/ -> output/
         \-> projects ->/
```

## Repository ownership

- `pi_workbench/` owns the new workbench CLI and Vault scaffold.
- `.skills/workbench-*/` owns Pi-specific workflows.
- `docs/workbench-*.md` defines the data contract and upstream-sync policy.
- `obsidian_wiki/` is inherited compatibility code. Do not alter it for a Pi Workbench behavior unless the change is deliberately upstream-compatible and tested against its existing suite.
- The user’s personal Vault never belongs in this repository; `/vault/` is intentionally ignored.

## Vault contract

A generated Vault has exactly these user-facing layers:

```text
_system/                 # Pi contract, templates, dashboards
raw/                     # journal, ideas, clips, subscriptions
wiki/                    # concepts, evidence, methods, decisions, entities, synthesis
projects/                # lightweight goal + Now work tables
output/                  # understanding, profile, content, products, portfolio
assets/
archive/
```

- Read `vault/_system/AGENTS.md` before any workbench read or write.
- Preserve raw inputs. They are original context, not a queue to clear.
- Wiki claims must retain source linkage and mark inference or uncertainty.
- Agent drafts in `output/` remain `draft`; only the user can mark material `owned`, `ready`, or `published`.
- A project is only for a bounded goal with intended output. Its `## Now` checklist is the MVP task system.

## Engineering rules

- Start with `git status --short --branch` and inspect the relevant module, tests, and docs.
- Keep changes local to the owning layer; preserve inherited upstream behavior unless a deliberate divergence is documented in `docs/upstream-policy.md`.
- Add or update focused tests for Pi Workbench behavior. Run the relevant test first, then the full suite when changing shared packaging or integration.
- Check `git diff --check` before handoff.
- Do not push, publish, sync a personal Vault, or run external posting actions without explicit user authorization.

## Upstream synchronization

- `upstream` is `Ar9av/obsidian-wiki`; `origin` is the user’s fork.
- Review upstream changes on `upstream-sync/*` branches. Never merge `upstream/main` blindly.
- Preserve the MIT license and upstream attribution.

## Origin reference

The repository began from an upstream MIT-licensed codebase, but Pi Workbench is now independent. The inherited `obsidian_wiki/` tree is reference material only: it is not packaged or a supported runtime dependency. Do not merge `upstream/main`; adapt a specific implementation into `pi_workbench/` only when there is a demonstrated Workbench need, a scope-aware design, and focused tests.

The legacy documentation tests may remain while the historical snapshot is present. They do not define Pi Workbench Vault behavior.

### Legacy snapshot test compatibility

The retained historical test suite still checks that its old docs have these literal upstream references: `wiki-context-pack`, `wiki-narrate`, `session-brain`, `session-search`, `/wiki-sessions`, `0. **Inline vault override (`@name`)**`, and `check_readme_sync.py`. They document the frozen reference snapshot only; they are not Pi Workbench Vault commands or supported runtime dependencies.

### Session history: ingest vs. retrieve

For that frozen upstream protocol, a missing named `@name` config: do **not** silently fall back to the default. Historical session history: ingest vs. retrieve is preserved in the reference docs, where `session-brain` / `session-search` retrieve a past session while history ingest writes a durable record.
