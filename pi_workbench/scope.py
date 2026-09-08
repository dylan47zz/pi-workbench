"""Canonical Pi Workbench vault selection and Markdown page parsing.

Every workbench capability gets its path semantics from this module.  Raw
sources, compiled knowledge, projects, and output are intentionally separate:
callers must opt in to raw material instead of accidentally treating it as
compiled knowledge.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Iterator, Literal

from pi_workbench.vault import OUTPUT_KINDS, RAW_KINDS, WIKI_KINDS

ScopeName = Literal["wiki", "projects", "output"]
COMPILED_SCOPES: tuple[ScopeName, ...] = ("wiki", "projects", "output")

_WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:[|#][^\]]*?)?\]\]")
_FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---(?:\r?\n|$)", re.DOTALL)
_H1_RE = re.compile(r"^[ ]{0,3}#\s+(.+?)\s*$", re.MULTILINE)
_HEADING_RE = re.compile(r"^[ ]{0,3}#{1,6}\s+(.+?)\s*$", re.MULTILINE)
_TOKEN_RE = re.compile(r"[\w./+#-]+", re.UNICODE)


@dataclass(frozen=True)
class Page:
    """A compiled Pi Workbench Markdown page."""

    path: str
    scope: ScopeName
    kind: str
    title: str
    metadata: dict[str, str | tuple[str, ...]]
    body: str

    @property
    def text(self) -> str:
        return f"{self.title}\n{self.body}"


def relative_path(vault: Path, path: Path) -> str:
    return path.resolve().relative_to(vault.resolve()).as_posix()


def _parse_frontmatter(text: str) -> tuple[dict[str, str | tuple[str, ...]], str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    values: dict[str, str | tuple[str, ...]] = {}
    lines = match.group(1).splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            index += 1
            continue
        key, raw = line.split(":", 1)
        key, value = key.strip(), raw.strip()
        if value.startswith("[") and value.endswith("]"):
            values[key] = tuple(item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip())
        elif value in {">", ">-", "|", "|-"}:
            block: list[str] = []
            cursor = index + 1
            while cursor < len(lines) and lines[cursor].startswith((" ", "\t")):
                block.append(lines[cursor].strip())
                cursor += 1
            values[key] = " ".join(part for part in block if part).strip()
            index = cursor
            continue
        elif not value:
            items: list[str] = []
            cursor = index + 1
            while cursor < len(lines) and lines[cursor].startswith((" ", "\t")):
                child = lines[cursor].strip()
                if child.startswith("- "):
                    items.append(child[2:].strip().strip("'\""))
                cursor += 1
            values[key] = tuple(item for item in items if item) if items else ""
            index = cursor
            continue
        else:
            values[key] = value.strip("'\"")
        index += 1
    return values, text[match.end():]


def _scope_for(relative: Path) -> tuple[ScopeName, str] | None:
    if not relative.parts:
        return None
    root = relative.parts[0]
    if root == "wiki" and len(relative.parts) >= 2 and relative.parts[1] in WIKI_KINDS:
        return "wiki", relative.parts[1]
    if root == "projects":
        return "projects", "projects"
    if root == "output" and len(relative.parts) >= 2 and relative.parts[1] in OUTPUT_KINDS:
        return "output", relative.parts[1]
    return None


def iter_raw_inputs(vault: Path, kinds: Iterable[str] | None = None) -> list[Path]:
    """Return retained raw files in a stable order, limited to supported kinds."""
    selected = set(kinds or RAW_KINDS)
    unknown = selected - set(RAW_KINDS)
    if unknown:
        raise ValueError(f"unknown raw kind(s): {', '.join(sorted(unknown))}")
    files: list[Path] = []
    for kind in RAW_KINDS:
        if kind not in selected:
            continue
        root = vault / "raw" / kind
        if root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return sorted(files)


def iter_compiled_paths(vault: Path, scopes: Iterable[ScopeName] | None = None) -> list[Path]:
    """Return current compiled pages; raw, system, assets, and archive never leak in."""
    selected = tuple(scopes or COMPILED_SCOPES)
    unknown = set(selected) - set(COMPILED_SCOPES)
    if unknown:
        raise ValueError(f"unknown compiled scope(s): {', '.join(sorted(unknown))}")
    paths: list[Path] = []
    for scope in selected:
        root = vault / scope
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            relative = path.relative_to(vault)
            if _scope_for(relative) is not None:
                paths.append(path)
    return sorted(paths)


def page_from_path(vault: Path, path: Path) -> Page:
    relative = path.relative_to(vault)
    descriptor = _scope_for(relative)
    if descriptor is None:
        raise ValueError(f"not a compiled workbench page: {relative.as_posix()}")
    scope, kind = descriptor
    text = path.read_text(encoding="utf-8", errors="replace")
    metadata, body = _parse_frontmatter(text)
    title_value = metadata.get("title", "")
    h1 = _H1_RE.search(body)
    title = str(title_value).strip() or (h1.group(1).strip() if h1 else path.stem)
    return Page(relative.as_posix(), scope, kind, title, metadata, body.strip())


def iter_compiled_pages(vault: Path, scopes: Iterable[ScopeName] | None = None) -> list[Page]:
    return [page_from_path(vault, path) for path in iter_compiled_paths(vault, scopes)]


def wikilinks(text: str) -> tuple[str, ...]:
    return tuple(match.strip() for match in _WIKILINK_RE.findall(text) if match.strip())


def headings(body: str) -> tuple[str, ...]:
    return tuple(match.group(1).strip().rstrip("#").strip() for match in _HEADING_RE.finditer(body))


def resolve_link(target: str, pages: Iterable[Page]) -> str | None:
    """Resolve a wikilink target to a compiled page path when unambiguous."""
    normalized = target.strip().removesuffix(".md").strip("/")
    page_list = list(pages)
    exact = [page.path.removesuffix(".md") for page in page_list if page.path.removesuffix(".md") == normalized]
    if len(exact) == 1:
        return exact[0] + ".md"
    # Obsidian permits short links. Resolve only unique stems to avoid invented edges.
    stem = Path(normalized).name
    matches = [page.path for page in page_list if Path(page.path).stem == stem]
    return matches[0] if len(matches) == 1 else None


def tokens(text: str) -> tuple[str, ...]:
    return tuple(token.casefold() for token in _TOKEN_RE.findall(text) if token)
