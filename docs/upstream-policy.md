# Upstream Origin and Independence Policy

Pi Workbench originated from [`Ar9av/obsidian-wiki`](https://github.com/Ar9av/obsidian-wiki), licensed under MIT. It retains the required license and attribution, but it is now an **independent project**, not an actively synchronized upstream fork.

## Historical baseline

- Origin snapshot: `fcb97dc7e436ea857e7d489466dbd50d3711817b` from `Ar9av/obsidian-wiki`.
- The `upstream` Git remote is retained only as historical reference.
- The inherited source tree may remain in this repository temporarily as a readable implementation and test reference; it is **not** packaged, installed, or used by the Pi Workbench runtime.

## No routine synchronization

Do not merge, rebase, or regularly sync `upstream/main` into Pi Workbench.

Pi Workbench changed the governing data model:

```text
raw/ -> wiki/ -> output/
         \-> projects ->/
```

Upstream assumptions such as root-level knowledge categories and `_raw/` promotion are incompatible with this lifecycle. A broad sync would reintroduce those assumptions and create semantic—not merely textual—conflicts.

## Selective reference only

When a concrete need exists, an upstream change may be studied and reimplemented or manually adapted in `pi_workbench/`. Typical candidates are:

- Markdown/frontmatter parsing correctness;
- wikilink normalization;
- atomic file-write or path-safety patterns;
- graph algorithms with a clearly useful Workbench interpretation.

A copied or adapted change must:

1. live under `pi_workbench/`;
2. use the Workbench scope model;
3. receive Pi Workbench-specific tests;
4. retain appropriate attribution when substantial code is reused.

Do not import or enable inherited `obsidian_wiki` runtime modules as a shortcut.

## Data separation

This repository contains framework code, skills, templates, tests, and documentation. Personal Vault data remains outside it and should be private. `/vault/` is ignored intentionally.
