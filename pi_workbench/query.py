"""Workbench-scoped retrieval and bounded context assembly."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from pi_workbench.scope import COMPILED_SCOPES, Page, ScopeName, iter_compiled_pages, tokens

STOP_WORDS = frozenset({"a", "an", "and", "are", "do", "for", "how", "in", "is", "of", "or", "the", "to", "what", "我", "的", "和", "是", "在"})


@dataclass(frozen=True)
class Hit:
    page: Page
    score: float
    reasons: tuple[str, ...]


def parse_scopes(raw: str | None) -> tuple[ScopeName, ...]:
    if not raw or raw == "compiled":
        return COMPILED_SCOPES
    aliases = {"knowledge": "wiki", "work": "projects", "deliverables": "output"}
    values = tuple(aliases.get(item.strip(), item.strip()) for item in raw.split(",") if item.strip())
    unknown = set(values) - set(COMPILED_SCOPES)
    if unknown:
        raise ValueError(f"unknown scope(s): {', '.join(sorted(unknown))}")
    return values  # type: ignore[return-value]


def _field(value: str | tuple[str, ...] | None) -> str:
    return " ".join(value) if isinstance(value, tuple) else str(value or "")


def rank(vault: Path, question: str, scopes: Iterable[ScopeName] | None = None, limit: int = 12) -> list[Hit]:
    terms = tuple(term for term in tokens(question) if term not in STOP_WORDS)
    if not terms:
        return []
    hits: list[Hit] = []
    for page in iter_compiled_pages(vault, scopes):
        title = page.title.casefold()
        summary = _field(page.metadata.get("summary")).casefold()
        tags = _field(page.metadata.get("tags")).casefold()
        body = page.body.casefold()
        path = page.path.casefold()
        score = 0.0
        reasons: list[str] = []
        phrase = question.strip().casefold()
        if phrase and phrase in title:
            score += 12.0
            reasons.append("title phrase")
        for term in terms:
            if term in title:
                score += 7.0
                reasons.append(f"title:{term}")
            if term in tags:
                score += 4.0
                reasons.append(f"tag:{term}")
            if term in summary:
                score += 3.0
                reasons.append(f"summary:{term}")
            if term in path:
                score += 2.0
                reasons.append(f"path:{term}")
            if term in body:
                score += 1.0
        if score:
            hits.append(Hit(page, score, tuple(dict.fromkeys(reasons))))
    hits.sort(key=lambda hit: (-hit.score, hit.page.path))
    return hits[:limit]


def _excerpt(page: Page, terms: tuple[str, ...], max_chars: int) -> str:
    body = page.body.strip()
    if not body:
        return ""
    lowered = body.casefold()
    positions = [lowered.find(term) for term in terms if lowered.find(term) >= 0]
    if not positions:
        return body[:max_chars].strip()
    start = max(0, min(positions) - max_chars // 3)
    end = min(len(body), start + max_chars)
    return body[start:end].strip()


def context_pack(vault: Path, topic: str, scopes: Iterable[ScopeName] | None = None, budget: int = 4_000) -> dict[str, object]:
    if budget < 256:
        raise ValueError("budget must be at least 256 characters")
    scope_values = tuple(scopes or COMPILED_SCOPES)
    hits = rank(vault, topic, scope_values, limit=20)
    terms = tuple(term for term in tokens(topic) if term not in STOP_WORDS)
    used = 0
    entries: list[dict[str, object]] = []
    for hit in hits:
        remaining = budget - used
        if remaining < 160:
            break
        excerpt = _excerpt(hit.page, terms, min(1_000, remaining))
        payload = {
            "path": hit.page.path,
            "scope": hit.page.scope,
            "title": hit.page.title,
            "score": round(hit.score, 2),
            "excerpt": excerpt,
        }
        entries.append(payload)
        used += len(hit.page.title) + len(excerpt)
    return {
        "topic": topic,
        "scopes": list(scope_values),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "budget_chars": budget,
        "used_chars": used,
        "pages": entries,
    }
