---
name: workbench-dashboard
description: >
  Build or refresh the Pi Workbench operational dashboard in `_system/dashboards`. Use when the user asks for a
  dashboard, Today view, overview, active-project view, signal view, content pipeline, or a visual workbench
  home. The dashboard summarizes raw signals, active projects, and draft output without converting raw count into
  a completion target.
---

# Workbench Dashboard

Read `_system/AGENTS.md`, then refresh the generated dashboard:

```bash
pi-workbench dashboard
```

The dashboard belongs in `_system/dashboards/now.md`. It is a generated view, not a source of truth. Authoritative content remains in `raw/`, `wiki/`, `projects/`, and `output/`.

If the user asks for a new custom view, use Obsidian Bases or Dataview only after confirming the needed metadata exists. Do not make category counts into productivity scores.
