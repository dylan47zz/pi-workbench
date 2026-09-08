# Pi Workbench Architecture

Pi Workbench is a Pi-agent personal operating layer over an Obsidian-compatible vault. It retains Markdown ownership and evidence-aware retrieval, then adds a direct path from personal information to work and expression.

## Lifecycle

```text
raw -> wiki -> output
         \-> projects ->/
```

- **Raw** preserves original context and does not need to be processed.
- **Wiki** is agent-searchable evidence, concepts, methods, decisions, entities, and synthesis.
- **Projects** are lightweight work tables with a bounded goal, `## Now`, evidence, and intended output.
- **Output** is where evidence becomes a human-owned explanation, profile asset, content draft, product document, or portfolio case.

## Vault layout

```text
personal-workbench/
├── _system/
│   ├── AGENTS.md
│   ├── templates/
│   └── dashboards/
├── raw/
│   ├── journal/
│   ├── ideas/
│   ├── clips/
│   └── subscriptions/
├── wiki/
│   ├── concepts/
│   ├── evidence/
│   ├── methods/
│   ├── decisions/
│   ├── entities/
│   └── synthesis/
├── projects/
├── output/
│   ├── understanding/
│   ├── profile/
│   ├── content/
│   ├── products/
│   └── portfolio/
├── assets/
└── archive/
```

## Invariants

1. A raw input needs only a category and filename; no tags or project are required.
2. Wiki claims link to raw sources or other evidence and mark inference or uncertainty.
3. A project exists only for a bounded goal with intended output. Its `## Now` section replaces a separate task system in the MVP.
4. Every substantial output links to Wiki evidence or project context.
5. An Agent draft is never represented as user-owned understanding or published external material.
6. Publishing, profile changes, and other external actions require explicit user confirmation.

## Configuration

Pi Workbench stores configuration at `$XDG_CONFIG_HOME/pi-workbench/config` (default `~/.config/pi-workbench/config`) and resolves the active Vault through `PI_WORKBENCH_VAULT_PATH`. This isolates it from any separately installed `obsidian-wiki` configuration.

## MVP CLI

```bash
pi-workbench setup --vault ~/Documents/personal-workbench
pi-workbench doctor
pi-workbench raw-status
pi-workbench install-pi-skills
```

## Operational capabilities

The MVP now includes native capture, triage, query, bounded context, project, output, status, lint, graph, review, dashboard, subscription, and focused history skills. Their migration status and the upstream features deliberately deferred are documented in [Skill Migration Map](skill-migration.md).
