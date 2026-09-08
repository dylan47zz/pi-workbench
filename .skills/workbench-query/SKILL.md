---
name: workbench-query
description: >
  Answer a question from a Pi Workbench vault's compiled material. Use when the user asks what they know,
  wants relevant evidence for a project, needs prior output or profile material, or asks how workbench topics
  connect. Search `wiki`, `projects`, and `output` by default; raw inputs are excluded unless the user explicitly
  asks to inspect them through workbench-triage.
---

# Workbench Query

Read `_system/AGENTS.md`, then use:

```bash
pi-workbench query "<question>" --scope compiled --json --pretty
```

Scopes:

- `wiki` — compiled concepts, evidence, methods, decisions, entities, synthesis;
- `projects` — current work tables;
- `output` — human-owned drafts and deliverables;
- `compiled` — all three.

Use the narrowest scope that answers the question. Cite the returned paths and clearly separate sourced material from your inference. Do not write during a query.

If the answer is likely only in `raw/`, say so and route to `workbench-triage`; do not silently treat raw text as verified knowledge.
