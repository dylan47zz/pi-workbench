---
name: workbench-triage
description: >
  Review selected Pi Workbench raw inputs and propose or stage their next useful destinations. Use when the
  user asks to triage captures, review journal/ideas/clips/subscriptions, find useful signals, or decide what
  should become knowledge, a project, or an output. Preserve raw originals and never use a staging-promotion
  workflow that moves these workbench inputs.
---

# Workbench Triage

Read `_system/AGENTS.md` first. `raw/` is retained source material, not a queue that must reach zero.

## Process

1. Inspect only requested raw files or one category.
2. For each input choose one outcome:
   - **retain** — useful context, but no present action;
   - **ignore** — no current value; leave original untouched;
   - **compile** — propose a source-backed update to `wiki/concepts/`, `wiki/evidence/`, `wiki/methods/`, `wiki/decisions/`, `wiki/synthesis/`, or `wiki/entities/`;
   - **work** — add a next action to an existing project’s `## Now`; create a project only for a bounded goal with intended output;
   - **express** — propose `output/understanding/`, `output/content/`, `output/profile/`, `output/products/`, or `output/portfolio/`.
3. State evidence and uncertainty for every compile/work/express proposal. Deduplicate against existing Wiki pages before proposing a new one.
4. Default to a concise review list. Write compiled pages only after user approval or a vault policy that explicitly permits drafts.

## Human ownership

For `output/understanding`, ask one high-information question before drafting: the user explains their judgment without rereading the source. An agent can draft but cannot mark an item `owned`, `ready`, or `published`.

## Completion

Report the chosen outcome and minimum next action per inspected input. Do not move or rewrite raw originals.
