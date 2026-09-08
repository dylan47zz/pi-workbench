---
name: workbench-status
description: >
  Show the operational state of a Pi Workbench vault: retained raw signals by category, active projects, compiled
  knowledge count, and output drafts awaiting human ownership. Use when the user asks what needs attention, what
  is active, their workbench status, their current projects, or pending output. Do not frame raw item count as a
  backlog that must be cleared.
---

# Workbench Status

Run:

```bash
pi-workbench status --json --pretty
```

Report in this order:

1. Raw signals by category, without implying every input needs processing;
2. active projects and their path;
3. output drafts needing a human ownership or publishing decision;
4. compiled knowledge count only as context, never as a productivity KPI.

Do not write while reporting status.
