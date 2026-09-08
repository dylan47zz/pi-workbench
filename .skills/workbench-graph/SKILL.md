---
name: workbench-graph
description: >
  Inspect the graph connecting Pi Workbench wiki pages, projects, and output. Use when the user asks what is
  connected, which pages are central, how a project relates to an output, or for a workbench graph. Raw inputs,
  system files, assets, and archive are excluded by design.
---

# Workbench Graph

Run:

```bash
pi-workbench graph --scope compiled --json --pretty
```

Use `wiki`, `projects`, `output`, or `compiled` scopes as needed. Interpret centrality as navigation context, not as importance or a productivity score. A graph edge means a Markdown link; it is not proof of causality.

Do not create links automatically from graph output. Suggest a small number of candidate links and ask before writing.
