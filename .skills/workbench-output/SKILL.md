---
name: workbench-output
description: >
  Turn Pi Workbench evidence or project context into a user-owned understanding, profile asset, content draft,
  product document, or portfolio case. Use when the user wants to form their own view, write a self-introduction,
  produce content, create a product brief, or derive a portfolio case from the vault. Preserve the distinction
  between agent drafts and human-owned output.
---

# Workbench Output

Read `_system/AGENTS.md`, then retrieve only relevant `wiki/` and project context. Do not treat raw material as verified knowledge.

## Route

- Personal explanation, mental model, or decision-ready view → `output/understanding/`.
- Self-introduction, bio, capability claim, or experience evidence → `output/profile/`.
- Topic, outline, draft, channel variant, or published copy → `output/content/`.
- PRD, product brief, technical proposal, or launch material → `output/products/`.
- Reusable project case → `output/portfolio/`.

## Ownership gate

An output starts with `status: draft`. The agent can link sources and label uncertainty, but the user alone can make it `owned`, `ready`, or `published`.

For `output/understanding`, prompt the user to explain first. Preserve:

1. `我的判断`
2. `为什么`
3. `边界与不确定性`
4. `下一次使用`

For profile and public content, separate verified evidence from positioning. Never invent metrics, ownership, publication, or outcomes.

## Completion

Return the draft path, linked evidence, unresolved uncertainty, and the user decision required for promotion.
