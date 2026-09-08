"""Current-work status for a Pi Workbench vault."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from pi_workbench.scope import iter_compiled_pages, iter_raw_inputs
from pi_workbench.vault import OUTPUT_KINDS, RAW_KINDS, raw_inventory


def _string(metadata: dict[str, str | tuple[str, ...]], key: str) -> str:
    value = metadata.get(key, "")
    return value if isinstance(value, str) else " ".join(value)


def snapshot(vault: Path) -> dict[str, object]:
    raw = raw_inventory(vault)
    pages = iter_compiled_pages(vault)
    projects = [page for page in pages if page.scope == "projects"]
    outputs = [page for page in pages if page.scope == "output"]
    wiki = [page for page in pages if page.scope == "wiki"]
    active_projects = [
        {"path": page.path, "title": page.title, "status": _string(page.metadata, "status") or "unknown"}
        for page in projects
        if (_string(page.metadata, "status") or "active") not in {"done", "archived", "cancelled"}
    ]
    output_status = Counter((_string(page.metadata, "status") or "unknown") for page in outputs)
    output_kinds = Counter(page.kind for page in outputs)
    draft_output = [
        {"path": page.path, "title": page.title, "kind": page.kind}
        for page in outputs
        if (_string(page.metadata, "status") or "draft") == "draft"
    ]
    return {
        "raw": raw,
        "compiled_pages": len(pages),
        "wiki_pages": len(wiki),
        "active_projects": active_projects,
        "output": {
            "by_status": dict(sorted(output_status.items())),
            "by_kind": {kind: output_kinds[kind] for kind in OUTPUT_KINDS},
            "drafts": draft_output,
        },
    }
