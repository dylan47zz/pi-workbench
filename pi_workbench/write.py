"""Safe, minimal writers for the workbench's user-facing pages."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from pi_workbench.vault import OUTPUT_KINDS, RAW_KINDS

_SLUG_RE = re.compile(r"[^\w\u4e00-\u9fff-]+", re.UNICODE)


def slugify(value: str) -> str:
    slug = _SLUG_RE.sub("-", value.strip().casefold()).strip("-_")
    if not slug or slug in {".", ".."}:
        raise ValueError("a non-empty title or slug is required")
    return slug[:80]


def _unique(path: Path) -> Path:
    if not path.exists():
        return path
    for number in range(2, 10_000):
        candidate = path.with_name(f"{path.stem}-{number}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not allocate a unique path for {path}")


def _frontmatter(title: str, fields: dict[str, str]) -> str:
    lines = ["---", "title: >-", f"  {title}"]
    lines.extend(f"{key}: {value}" for key, value in fields.items())
    lines.append("---")
    return "\n".join(lines)


def capture_raw(
    vault: Path,
    *,
    kind: str,
    title: str,
    text: str,
    source: str | None = None,
    why: str | None = None,
    captured_at: datetime | None = None,
) -> Path:
    if kind not in RAW_KINDS:
        raise ValueError(f"unknown raw kind: {kind}")
    now = captured_at or datetime.now()
    path = _unique(vault / "raw" / kind / f"{now.date().isoformat()}-{slugify(title)}.md")
    sections = [f"# {title}", ""]
    if source:
        sections += [f"来源：{source}", ""]
    if why:
        sections += [f"为什么保存：{why}", ""]
    sections.append(text.strip())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return path


def create_project(vault: Path, *, slug: str, title: str, goal: str, intended_output: str = "") -> Path:
    path = _unique(vault / "projects" / f"{slugify(slug)}.md")
    today = datetime.now().date().isoformat()
    front = _frontmatter(title, {"type": "project", "status": "active", "created": today, "updated": today})
    output_link = _workbench_link(intended_output)
    body = f"""
# {title}

## Goal

{goal.strip()}

## Now

- [ ] Define the next concrete action

## Current judgment

## Evidence and context

## Intended output

{output_link}

## Review
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front + body, encoding="utf-8")
    return path


def _workbench_link(path: str) -> str:
    normalized = path.strip().removesuffix(".md")
    return f"[[{normalized}]]" if normalized else ""


def create_output(vault: Path, *, kind: str, slug: str, title: str, source: str = "") -> Path:
    if kind not in OUTPUT_KINDS:
        raise ValueError(f"unknown output kind: {kind}")
    path = _unique(vault / "output" / kind / f"{slugify(slug)}.md")
    today = datetime.now().date().isoformat()
    front = _frontmatter(title, {"type": f"output-{kind}", "status": "draft", "created": today, "updated": today, "sources": "[]"})
    source_link = _workbench_link(source)
    bodies = {
        "understanding": """
# {title}

## 我的判断

## 为什么

## 边界与不确定性

## 下一次使用

## 证据与上下文

{source_link}
""",
        "profile": """
# {title}

## 可信主张

## 证据

## 场景版本

## 待确认

## 证据与上下文

{source_link}
""",
        "content": """
# {title}

## 面向谁

## 核心主张

## 证据与例子

## 草稿

## 渠道版本

## 证据与上下文

{source_link}
""",
        "products": """
# {title}

## 问题与目标

## 当前方案

## 证据与约束

## 决策与下一步

## 证据与上下文

{source_link}
""",
        "portfolio": """
# {title}

## 背景与目标

## 我的贡献

## 方法与取舍

## 结果与证据

## 复盘

## 证据与上下文

{source_link}
""",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front + bodies[kind].format(title=title, source_link=source_link), encoding="utf-8")
    return path
