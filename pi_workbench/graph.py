"""Scoped graph view over compiled Pi Workbench pages."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from pi_workbench.scope import COMPILED_SCOPES, Page, ScopeName, iter_compiled_pages, resolve_link, wikilinks


def build(vault: Path, scopes: Iterable[ScopeName] | None = None) -> dict[str, object]:
    scope_values = tuple(scopes or COMPILED_SCOPES)
    pages = iter_compiled_pages(vault, scope_values)
    edges: list[dict[str, str]] = []
    incoming: dict[str, int] = {page.path: 0 for page in pages}
    outgoing: dict[str, int] = {page.path: 0 for page in pages}
    for page in pages:
        for target in wikilinks(page.body):
            resolved = resolve_link(target, pages)
            if not resolved or resolved == page.path:
                continue
            edges.append({"source": page.path, "target": resolved})
            outgoing[page.path] += 1
            incoming[resolved] += 1
    nodes = [
        {
            "path": page.path,
            "title": page.title,
            "scope": page.scope,
            "kind": page.kind,
            "incoming": incoming[page.path],
            "outgoing": outgoing[page.path],
        }
        for page in pages
    ]
    nodes.sort(key=lambda node: (-(node["incoming"] + node["outgoing"]), node["path"]))
    return {"scopes": list(scope_values), "nodes": nodes, "edges": edges, "stats": {"pages": len(nodes), "edges": len(edges)}}
