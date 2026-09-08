r"""Pi Workbench vault contract.

The vault is deliberately arranged around the user-facing lifecycle, not an
upstream wiki's internal conventions:

    raw -> wiki -> output
             \-> projects ->/
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

RAW_KINDS = ("journal", "ideas", "clips", "subscriptions")
WIKI_KINDS = ("concepts", "evidence", "methods", "decisions", "entities", "synthesis")
OUTPUT_KINDS = ("understanding", "profile", "content", "products", "portfolio")

VAULT_DIRS = (
    "_system/templates",
    "_system/dashboards",
    *(f"raw/{kind}" for kind in RAW_KINDS),
    *(f"wiki/{kind}" for kind in WIKI_KINDS),
    "projects",
    *(f"output/{kind}" for kind in OUTPUT_KINDS),
    "assets",
    "archive",
    ".obsidian",
)

SYSTEM_AGENTS_TEMPLATE = """# Pi Workbench Contract

This vault is a personal workbench. Its lifecycle is `raw -> wiki -> output`.
Projects are lightweight working tables that connect those layers; they are not a second task system.

## Paths and roles

- `raw/` is the only input layer. It retains original wording and context.
  - `raw/journal/`: personal or work log, meeting aftermath, observations.
  - `raw/ideas/`: a question, hypothesis, or undeveloped direction.
  - `raw/clips/`: manual web, document, screenshot, or quote capture.
  - `raw/subscriptions/`: RSS, newsletter, and recurring information inputs.
- `wiki/` is compiled, agent-searchable knowledge.
  - `concepts/`, `evidence/`, `methods/`, `decisions/`, `entities/`, `synthesis/`.
- `projects/` holds only bounded goals. A project page contains `## Goal`, `## Now`, evidence, and intended output.
- `output/` holds human-owned results: understanding, profile material, content, product documents, and portfolio cases.
- `archive/` holds retired projects or superseded outputs. Do not use it as an input queue.
- `_system/` holds Pi instructions, templates, and dashboards. It is not a knowledge destination.

## Capture and triage

Capture without tags, project assignment, or a complete template. Preserve raw files after analysis.
For each reviewed raw item, choose one outcome: retain, ignore, compile into `wiki/`, add to a project, or express through `output/`.

## Evidence and ownership

- Wiki claims link to raw sources or other evidence and distinguish extracted facts from inference.
- An agent may draft an item in `output/`, but only the user can mark it `owned`, `ready`, or `published`.
- Before drafting `output/understanding`, prompt the user to explain their view first.
- An understanding note uses: `我的判断`, `为什么`, `边界与不确定性`, `下一次使用`.
- Publishing, sending, or changing an external profile requires an explicit user instruction in the current conversation.

## Working style

Keep the system low-friction. Do not turn every capture into a task, project, tag, or note rewrite.
Create a project only when there is a bounded goal and expected output. Use its `## Now` checklist before introducing separate task files.
"""

HOME_TEMPLATE = """---
title: >-
  Pi Workbench Home
---

# Pi Workbench

## Capture

- [[raw/journal/]] — daily context and observations
- [[raw/ideas/]] — questions and hypotheses
- [[raw/clips/]] — manual captures
- [[raw/subscriptions/]] — recurring information inputs

## Work tables

- [[projects/]] — bounded work with a goal and `## Now`
- [[output/]] — human-owned understanding and deliverables

## Knowledge base

- [[wiki/concepts/]] · [[wiki/evidence/]] · [[wiki/methods/]] · [[wiki/decisions/]] · [[wiki/entities/]] · [[wiki/synthesis/]]

> [!note]
> The workbench succeeds when information becomes a decision, a project outcome, or an expression you can own—not when every input is processed.
"""

PROJECT_TEMPLATE = """---
title: >-
  <Project title>
type: project
status: active
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Project title>

## Goal

## Now

- [ ] One concrete next action

## Current judgment

## Evidence and context

## Intended output

## Review
"""

UNDERSTANDING_TEMPLATE = """---
title: >-
  <Topic>
type: personal-understanding
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
---

# <Topic>

## 我的判断

## 为什么

## 边界与不确定性

## 下一次使用
"""

RAW_TEMPLATES = {
    "journal": "# YYYY-MM-DD\n\n## 发生了什么\n\n## 卡点或反复出现的问题\n\n## 我想保留的线索\n",
    "ideas": "# 一个问题或方向\n\n我为什么现在想到它：\n\n下一步（可留空）：\n",
    "clips": "# 标题\n\n来源：\n\n我为什么保存：\n\n摘录或附件：\n",
    "subscriptions": "# 标题\n\n来源：\n日期：\n\n信号：\n\n为什么可能与我有关：\n",
}


def _write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def scaffold(vault: Path) -> bool:
    """Create the workbench structure without overwriting user content."""
    created = not vault.is_dir()
    for relative in VAULT_DIRS:
        (vault / relative).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write_if_missing(vault / "_system/AGENTS.md", SYSTEM_AGENTS_TEMPLATE)
    _write_if_missing(vault / "_system/dashboards/home.md", HOME_TEMPLATE)
    _write_if_missing(vault / "_system/templates/project.md", PROJECT_TEMPLATE)
    _write_if_missing(vault / "_system/templates/personal-understanding.md", UNDERSTANDING_TEMPLATE)
    for kind, template in RAW_TEMPLATES.items():
        _write_if_missing(vault / "_system/templates" / f"raw-{kind}.md", template)
    _write_if_missing(vault / "_system/workbench-log.md", f"# Workbench Log\n\n- [{timestamp}] INIT vault_path=\"{vault}\"\n")
    _write_if_missing(vault / ".obsidian/app.json", '{\n  "defaultViewMode": "preview",\n  "livePreview": true\n}\n')
    return created


def raw_inventory(vault: Path) -> dict[str, object]:
    """Return a non-mutating inventory of retained raw inputs by category."""
    root = vault / "raw"
    counts: Counter[str] = Counter()
    files: dict[str, list[str]] = {kind: [] for kind in RAW_KINDS}
    uncategorized: list[str] = []
    if not root.is_dir():
        return {"root": str(root), "counts": {kind: 0 for kind in RAW_KINDS}, "files": files, "uncategorized": [], "total": 0}

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        kind = relative.parts[0] if len(relative.parts) > 1 else ""
        target = relative.as_posix()
        if kind in RAW_KINDS:
            counts[kind] += 1
            files[kind].append(target)
        else:
            uncategorized.append(target)

    return {
        "root": str(root),
        "counts": {kind: counts[kind] for kind in RAW_KINDS},
        "files": files,
        "uncategorized": uncategorized,
        "total": sum(counts.values()) + len(uncategorized),
    }
