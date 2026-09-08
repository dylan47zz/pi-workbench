from __future__ import annotations

import json
from pathlib import Path

from pi_workbench import cli
from pi_workbench.config import config_path, resolve_vault
from pi_workbench.lint import report as lint_report
from pi_workbench.query import context_pack, rank
from pi_workbench.scope import iter_compiled_pages, iter_raw_inputs
from pi_workbench.status import snapshot
from pi_workbench.vault import OUTPUT_KINDS, RAW_KINDS, WIKI_KINDS, raw_inventory, scaffold


def write(vault: Path, relative: str, text: str) -> Path:
    path = vault / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def page(*, title: str, body: str, type_: str = "note", status: str = "draft", sources: str = "[raw/clips/source.md]") -> str:
    return f"""---
title: >-
  {title}
type: {type_}
category: note
status: {status}
sources: {sources}
created: 2026-09-08
updated: 2026-09-08
summary: >-
  {title} summary
---

# {title}

{body}
"""


def test_scaffold_creates_explicit_workbench_shape_without_overwriting_raw_note(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    assert scaffold(vault) is True
    assert scaffold(vault) is False

    for relative in (
        "_system/AGENTS.md",
        "_system/dashboards/home.md",
        "_system/templates/project.md",
        "raw/journal",
        "raw/ideas",
        "raw/clips",
        "raw/subscriptions",
        "wiki",
        *(f"wiki/{kind}" for kind in WIKI_KINDS),
        "projects",
        "output/understanding",
        "output/profile",
        "output/content",
        "output/products",
        "output/portfolio",
        "assets",
        "archive",
    ):
        assert (vault / relative).exists(), relative

    journal = vault / "raw/journal/keep.md"
    journal.write_text("personal source\n", encoding="utf-8")
    scaffold(vault)
    assert journal.read_text(encoding="utf-8") == "personal source\n"
    assert not (vault / "_raw").exists()
    assert not (vault / "concepts").exists()


def test_raw_inventory_counts_nested_categories_without_system_folders(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    scaffold(vault)
    write(vault, "raw/journal/day.md", "x")
    write(vault, "raw/ideas/question.md", "x")
    write(vault, "raw/clips/paper.md", "x")
    write(vault, "raw/subscriptions/feed/news.md", "x")
    write(vault, "raw/loose.md", "x")

    inventory = raw_inventory(vault)

    assert inventory["counts"] == {kind: 1 for kind in RAW_KINDS}
    assert inventory["total"] == 5
    assert inventory["uncategorized"] == ["loose.md"]
    assert inventory["files"]["subscriptions"] == ["subscriptions/feed/news.md"]
    assert [path.relative_to(vault).as_posix() for path in iter_raw_inputs(vault, ["ideas"])] == ["raw/ideas/question.md"]


def test_scope_query_context_status_and_lint_follow_workbench_boundaries(tmp_path: Path, capsys) -> None:
    vault = tmp_path / "vault"
    scaffold(vault)
    write(vault, "raw/clips/source.md", "# Raw research\nAgent workbench signal\n")
    write(vault, "wiki/concepts/agent-workbench.md", page(title="Agent Workbench", body="A system turns evidence into human-owned output. [[projects/pi-workbench]]", sources="[raw/clips/source.md]"))
    write(vault, "projects/pi-workbench.md", page(title="Pi Workbench", type_="project", status="active", body="## Goal\nBuild a workbench.\n\n## Now\n- [ ] Ship query\n\n## Intended output\n[[output/products/pi-workbench-mvp]]\n", sources="[wiki/concepts/agent-workbench.md]"))
    write(vault, "output/products/pi-workbench-mvp.md", page(title="Pi Workbench MVP", type_="product-document", body="A product proposal built from [[wiki/concepts/agent-workbench]].", sources="[projects/pi-workbench.md]"))
    write(vault, "_system/dashboards/noise.md", "# Not knowledge\n")
    write(vault, "archive/old.md", "# Archived\n")

    pages = iter_compiled_pages(vault)
    assert {page.path for page in pages} == {
        "wiki/concepts/agent-workbench.md",
        "projects/pi-workbench.md",
        "output/products/pi-workbench-mvp.md",
    }
    hits = rank(vault, "agent workbench")
    assert hits[0].page.path == "wiki/concepts/agent-workbench.md"
    assert "raw/clips/source.md" not in {hit.page.path for hit in hits}
    pack = context_pack(vault, "agent workbench", budget=900)
    assert pack["pages"]
    assert all(item["path"].split("/", 1)[0] in {"wiki", "projects", "output"} for item in pack["pages"])
    state = snapshot(vault)
    assert state["raw"]["counts"]["clips"] == 1
    assert state["active_projects"][0]["path"] == "projects/pi-workbench.md"
    assert lint_report(vault)["status"] == "pass"
    assert cli.main(["graph", "--vault", str(vault), "--json"]) == 0
    graph = json.loads(capsys.readouterr().out)
    assert graph["stats"] == {"pages": 3, "edges": 3}
    assert cli.main(["review", "--vault", str(vault), "--json"]) == 0
    review = json.loads(capsys.readouterr().out)
    assert review["recent_raw"] == ["raw/clips/source.md"]
    assert cli.main(["dashboard", "--vault", str(vault)]) == 0
    dashboard_path = vault / capsys.readouterr().out.strip()
    assert dashboard_path.exists()
    assert "Pi Workbench Now" in dashboard_path.read_text(encoding="utf-8")


def test_cli_writers_create_linked_project_and_output(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("PI_WORKBENCH_CONFIG_DIR", str(tmp_path / "config"))
    vault = tmp_path / "vault"
    assert cli.main(["setup", "--vault", str(vault)]) == 0
    capsys.readouterr()
    assert cli.main(["output", "products", "mvp", "MVP"]) == 0
    output_path = capsys.readouterr().out.strip()
    assert output_path == "output/products/mvp.md"
    assert cli.main(["project", "build", "Build", "Ship MVP", "--intended-output", output_path]) == 0
    project_path = vault / capsys.readouterr().out.strip()
    assert "[[output/products/mvp]]" in project_path.read_text(encoding="utf-8")
    assert cli.main(["output", "understanding", "view", "My View", "--source", "projects/build.md"]) == 0
    understanding_path = vault / capsys.readouterr().out.strip()
    assert "[[projects/build]]" in understanding_path.read_text(encoding="utf-8")


def test_lint_requires_understanding_sections_and_compiled_links(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    scaffold(vault)
    write(vault, "output/understanding/incomplete.md", page(title="Incomplete", type_="personal-understanding", body="## 我的判断\nA claim.\n[[wiki/concepts/missing]]"))

    findings = lint_report(vault)

    rules = {issue["rule"] for issue in findings["issues"]}
    assert "understanding-contract" in rules
    assert "broken-link" in rules


def test_setup_uses_independent_config_and_cli_commands_read_it(tmp_path: Path, monkeypatch, capsys) -> None:
    config_dir = tmp_path / "config"
    vault = tmp_path / "vault"
    monkeypatch.setenv("PI_WORKBENCH_CONFIG_DIR", str(config_dir))

    assert cli.main(["setup", "--vault", str(vault)]) == 0
    capsys.readouterr()
    config = config_path()
    assert config.exists()
    assert 'PI_WORKBENCH_VAULT_PATH="' in config.read_text(encoding="utf-8")
    assert resolve_vault() == vault.resolve()

    write(vault, "raw/ideas/test.md", "x")
    write(vault, "wiki/concepts/test.md", page(title="Test idea", body="A test workbench idea."))
    assert cli.main(["raw-status", "--json", "--pretty"]) == 0
    raw = json.loads(capsys.readouterr().out)
    assert raw["counts"]["ideas"] == 1
    assert cli.main(["query", "test idea", "--json"]) == 0
    query = json.loads(capsys.readouterr().out)
    assert query["hits"][0]["path"] == "wiki/concepts/test.md"
    assert cli.main(["context", "test idea", "--json"]) == 0
    context = json.loads(capsys.readouterr().out)
    assert context["pages"][0]["path"] == "wiki/concepts/test.md"
    assert cli.main(["status", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["compiled_pages"] == 1
    assert cli.main(["lint", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "pass"


def test_doctor_fails_when_a_required_raw_kind_is_missing(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PI_WORKBENCH_CONFIG_DIR", str(tmp_path / "config"))
    vault = tmp_path / "vault"
    assert cli.main(["setup", "--vault", str(vault)]) == 0
    (vault / "raw/subscriptions").rmdir()

    assert cli.main(["doctor", "--vault", str(vault)]) == 1


def test_install_pi_skills_installs_all_workbench_skills(tmp_path: Path, capsys) -> None:
    target = tmp_path / "pi-skills"
    assert cli.main(["install-pi-skills", "--target", str(target)]) == 0
    installed = sorted(path.name for path in target.iterdir())
    assert installed == [
        "workbench-capture",
        "workbench-context",
        "workbench-dashboard",
        "workbench-graph",
        "workbench-history",
        "workbench-lint",
        "workbench-output",
        "workbench-project",
        "workbench-query",
        "workbench-review",
        "workbench-status",
        "workbench-subscriptions",
        "workbench-triage",
    ]
    assert all((target / skill / "SKILL.md").is_file() for skill in installed)
    assert "Installed 13 Pi Workbench skill(s)" in capsys.readouterr().out
