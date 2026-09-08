---
name: workbench-review
description: >
  Run a low-friction Pi Workbench review that turns recent signals into reflection questions. Use when the user
  asks for a daily review, weekly review, what to reflect on, what matters this week, or a workbench review. It
  should surface signals, active projects, and draft outputs without requiring a full raw inbox cleanup.
---

# Workbench Review

Run:

```bash
pi-workbench review --json --pretty
```

Ask at most three high-information questions selected from the returned signals. Prefer:

1. Which input changes a current judgment, project, or output?
2. Which draft needs the user's own explanation, evidence boundary, or next use?
3. Which project `## Now` is no longer the smallest useful action?

Do not convert review into a recurring note-count or inbox-zero ritual.
