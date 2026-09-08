"""Non-mutating weekly/daily review material for the workbench."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from pi_workbench.scope import iter_raw_inputs
from pi_workbench.status import snapshot


def build(vault: Path, *, raw_limit: int = 12) -> dict[str, object]:
    state = snapshot(vault)
    raw_paths = iter_raw_inputs(vault)
    recent_raw = sorted(raw_paths, key=lambda path: path.stat().st_mtime, reverse=True)[:raw_limit]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": state,
        "recent_raw": [path.relative_to(vault).as_posix() for path in recent_raw],
        "prompts": [
            "哪些 raw 信号真正改变了当前项目、判断或输出？",
            "哪个 output 草稿值得由我亲自补上判断、边界和下一次使用？",
            "哪个项目的 ## Now 已不再是最小有效下一步？",
        ],
    }
