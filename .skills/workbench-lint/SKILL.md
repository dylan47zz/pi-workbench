---
name: workbench-lint
description: >
  Validate Pi Workbench compiled pages against the raw/wiki/projects/output contract. Use when the user asks to
  check the workbench, validate links, find structural drift, review missing evidence metadata, or verify that
  project and understanding pages satisfy their templates. Raw inputs are intentionally out of scope.
---

# Workbench Lint

Run:

```bash
pi-workbench lint --json --pretty
```

The lint checks only compiled pages:

- Wiki pages need source-oriented metadata;
- project pages need Goal, Now, and Intended output;
- output pages need human ownership metadata;
- understanding pages additionally need 我的判断, 为什么, 边界与不确定性, 下一次使用;
- links to compiled paths must resolve.

Present findings first. Apply fixes only after the user approves the scope.
