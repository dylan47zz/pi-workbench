---
name: workbench-history
description: >
  Selectively recover durable knowledge from Pi or other agent session history into a Pi Workbench vault. Use when
  the user asks what they previously worked on, wants to mine a named Pi session/topic, import a focused slice of
  agent history, or retrieve a prior decision. Extract only source-backed outcomes into raw or wiki; do not bulk
  ingest all session history by default.
---

# Workbench History

Start with the specific topic or project the user needs. Locate relevant sessions first; do not bulk ingest history.

For selected material:

1. preserve a source locator under `raw/clips/` or an external session reference;
2. extract only verified decisions, reusable methods, concrete evidence, and unresolved questions;
3. route resulting knowledge through `workbench-triage`;
4. write a Wiki page only when the result has durable value beyond the session;
5. never place model reasoning or raw tool payloads into Wiki or Output.

If the user needs a past session merely to continue work, retrieve it without writing to the Vault.
