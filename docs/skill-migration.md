# Upstream Skill Migration Map

Pi Workbench does not rename or port every `obsidian-wiki` skill. It first gives the necessary capabilities a shared `raw/wiki/projects/output` scope, then keeps, adapts, or defers upstream features according to the personal-workbench lifecycle.

## Native workbench skills

| Skill | Status | Purpose |
|---|---|---|
| `workbench-capture` | active | Save low-friction journal, idea, clip, or subscription input under `raw/`. |
| `workbench-triage` | active | Retain, ignore, compile, work, or express selected raw input without moving the original. |
| `workbench-query` | active | Search `wiki/`, `projects/`, and `output/`; raw is excluded by default. |
| `workbench-context` | active | Build a bounded downstream context pack from compiled pages. |
| `workbench-project` | active | Maintain one lightweight project work table with Goal, Now, evidence, and intended output. |
| `workbench-output` | active | Draft understanding, profile, content, product, or portfolio output with a human ownership gate. |
| `workbench-status` | active | Show raw signals, active projects, and output drafts without inbox-zero pressure. |
| `workbench-lint` | active | Validate compiled page contracts and links. |
| `workbench-graph` | active | Inspect links across Wiki, projects, and output. |
| `workbench-review` | active | Ask a few high-information reflection questions. |
| `workbench-dashboard` | active | Generate the current operational dashboard under `_system/dashboards/`. |
| `workbench-subscriptions` | active | Triage recurring information by decision/project/output relevance. |
| `workbench-history` | active | Retrieve focused Agent history without bulk importing it. |

## Retained as reusable implementation or reference

| Upstream capability | Current handling |
|---|---|
| GraphRAG, context pack, graph analysis | Reimplemented behind `pi_workbench.scope`; only compiled workbench pages are selected. |
| Manifest/hash cache, code understanding, session search | Retained upstream code for later use; not a default Pi Workbench workflow yet. |
| Obsidian layout adjustment, Git sync | Remain optional utilities and do not affect the workbench lifecycle. |
| Skill creator, implementation validator | General engineering utilities; no vault-path migration required. |

## Deferred until a real need appears

| Upstream skill family | Why deferred |
|---|---|
| Bulk Claude/Codex/Copilot/Hermes/OpenClaw history ingest | A personal workbench should not import every conversation before the triage-to-output loop proves useful. |
| Dedup, cross-linker, synthesis automation | Useful only after a meaningful amount of compiled Wiki exists; automatic writes would be premature now. |
| Multi-vault switching, deployment/MCP server, browser extension, QMD | Infrastructure complexity without evidence of a current bottleneck. |
| Generic raw promotion and rebuild | Contradict raw retention and human-owned output semantics. |

## Compatibility rule

Do not invoke inherited `wiki-*` skills against a Pi Workbench Vault unless that skill has been explicitly migrated to `pi_workbench.scope`. Inherited skills still assume upstream root categories and `_raw/` staging.
