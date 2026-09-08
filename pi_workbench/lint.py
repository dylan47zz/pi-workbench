"""Structural lint for the Pi Workbench contract."""

from __future__ import annotations

from pathlib import Path

from pi_workbench.scope import headings, iter_compiled_pages, resolve_link, wikilinks


def _string(metadata: dict[str, str | tuple[str, ...]], key: str) -> str:
    value = metadata.get(key, "")
    return value if isinstance(value, str) else " ".join(value)


def _missing(page, fields: tuple[str, ...]) -> list[str]:
    return [field for field in fields if not _string(page.metadata, field)]


def report(vault: Path) -> dict[str, object]:
    pages = iter_compiled_pages(vault)
    issues: list[dict[str, object]] = []
    for page in pages:
        if page.scope == "wiki":
            missing = _missing(page, ("title", "category", "sources", "created", "updated"))
            if missing:
                issues.append({"path": page.path, "rule": "wiki-frontmatter", "missing": missing})
        elif page.scope == "projects":
            missing = _missing(page, ("title", "type", "status", "created", "updated"))
            missing_headings = [heading for heading in ("Goal", "Now", "Intended output") if heading not in headings(page.body)]
            if missing or missing_headings:
                issues.append({"path": page.path, "rule": "project-contract", "missing": missing, "missing_headings": missing_headings})
        elif page.scope == "output":
            missing = _missing(page, ("title", "type", "status", "created", "updated"))
            if missing:
                issues.append({"path": page.path, "rule": "output-frontmatter", "missing": missing})
            if page.kind == "understanding":
                missing_headings = [heading for heading in ("我的判断", "为什么", "边界与不确定性", "下一次使用") if heading not in headings(page.body)]
                if missing_headings:
                    issues.append({"path": page.path, "rule": "understanding-contract", "missing_headings": missing_headings})

        for target in wikilinks(page.body):
            if target.startswith(("raw/", "assets/")):
                continue
            if resolve_link(target, pages) is None:
                issues.append({"path": page.path, "rule": "broken-link", "target": target})

    return {"status": "pass" if not issues else "warn", "pages_checked": len(pages), "issues": issues}
