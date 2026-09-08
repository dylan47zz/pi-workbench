"""Generated Markdown dashboard for the current workbench state."""

from __future__ import annotations

from pathlib import Path

from pi_workbench.status import snapshot


def render(vault: Path) -> str:
    state = snapshot(vault)
    raw = state["raw"]
    active = state["active_projects"]
    drafts = state["output"]["drafts"]
    lines = [
        "---",
        "title: >-",
        "  Pi Workbench Now",
        "generated: true",
        "---",
        "",
        "# Pi Workbench Now",
        "",
        "## Signals",
        "",
    ]
    for kind, count in raw["counts"].items():
        lines.append(f"- `raw/{kind}`: {count}")
    lines += ["", "## Active projects", ""]
    if active:
        lines.extend(f"- [[{project['path'][:-3]}|{project['title']}]]" for project in active)
    else:
        lines.append("- No active project pages yet.")
    lines += ["", "## Draft output awaiting human ownership", ""]
    if drafts:
        lines.extend(f"- [[{draft['path'][:-3]}|{draft['title']}]] — {draft['kind']}" for draft in drafts)
    else:
        lines.append("- No output drafts awaiting review.")
    lines += [
        "",
        "## Review prompt",
        "",
        "> Which signal should change a judgment, project, or output this week?",
        "",
        f"Compiled pages: {state['compiled_pages']}.",
    ]
    return "\n".join(lines) + "\n"


def write(vault: Path) -> Path:
    path = vault / "_system" / "dashboards" / "now.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(vault), encoding="utf-8")
    return path
