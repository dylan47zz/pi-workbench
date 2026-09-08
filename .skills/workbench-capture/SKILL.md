---
name: workbench-capture
description: >
  Capture a user's journal entry, idea, web/document clip, or subscription signal into a Pi Workbench vault.
  Use when the user asks to save a thought, record a journal entry, capture an idea, clip a resource, or save
  a newsletter/RSS item for later. Route only to `raw/journal`, `raw/ideas`, `raw/clips`, or
  `raw/subscriptions`; preserve the input rather than compiling it into knowledge.
---

# Workbench Capture

Resolve the vault from `PI_WORKBENCH_VAULT_PATH`, then read `_system/AGENTS.md`.

## Route

- Personal/work record, meeting aftermath, observation → `raw/journal/`.
- Question, hypothesis, direction, or undeveloped thought → `raw/ideas/`.
- Manual page, document, screenshot, quote, or resource → `raw/clips/`.
- Recurring feed, newsletter, RSS item, or industry update → `raw/subscriptions/`.

Use `YYYY-MM-DD-<short-slug>.md`. Do not require tags, a project, or complete metadata before saving. Preserve original wording. For a clip or subscription, retain URL, author/date when available, and why it might matter.

## Completion

Confirm the exact path and selected raw kind. Do not create Wiki, project, or output pages during capture.
