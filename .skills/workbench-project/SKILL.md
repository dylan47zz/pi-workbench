---
name: workbench-project
description: >
  Create, update, or review a lightweight Pi Workbench project page. Use when the user starts a bounded project,
  asks what to do next on a project, wants to connect evidence to a product/content goal, or needs a project
  review. A project is one Markdown work table with Goal, Now, Evidence and context, Intended output, and Review;
  do not create a separate task database.
---

# Workbench Project

Read `_system/AGENTS.md`. A project belongs in `projects/` only when it has a bounded goal and an intended output.

## Create or update

Use `_system/templates/project.md`. Maintain these sections:

- `## Goal` — concrete outcome and boundary;
- `## Now` — one to three actionable checkboxes;
- `## Current judgment` — what is believed and why;
- `## Evidence and context` — links to `wiki/`, `raw/`, and relevant output;
- `## Intended output` — expected path(s) under `output/`;
- `## Review` — what was learned or remains unresolved.

Prefer an existing project page over a new one. Keep project status in frontmatter. Never auto-close a project or change its intended output without the user.

## Completion

Summarize the updated Goal, the current `Now`, linked evidence, and the next decision required from the user.
