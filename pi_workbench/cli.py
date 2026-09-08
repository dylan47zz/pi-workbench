"""CLI for scaffolding and inspecting a Pi Workbench vault."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from pi_workbench import __version__
from pi_workbench.config import config_path, resolve_vault, write_config
from pi_workbench.dashboard import write as write_dashboard
from pi_workbench.graph import build as graph_build
from pi_workbench.lint import report as lint_report
from pi_workbench.review import build as review_build
from pi_workbench.write import capture_raw, create_output, create_project
from pi_workbench.query import context_pack, parse_scopes, rank
from pi_workbench.status import snapshot as status_snapshot
from pi_workbench.vault import OUTPUT_KINDS, RAW_KINDS, raw_inventory, scaffold


def _skills_dir() -> Path:
    package_dir = Path(__file__).resolve().parent
    for candidate in (package_dir / "_data" / "skills", package_dir.parent / ".skills"):
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("Pi Workbench skills were not found; reinstall pi-workbench.")


def _required_paths(vault: Path) -> list[Path]:
    required = ["_system/AGENTS.md", "_system/dashboards/home.md", "_system/workbench-log.md"]
    required += [f"raw/{kind}" for kind in RAW_KINDS]
    required += ["wiki", "projects", "output", "assets", "archive", "_system/templates"]
    return [vault / relative for relative in required]


def cmd_setup(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    created = scaffold(vault)
    config = write_config(vault, __version__)
    verb = "created" if created else "verified"
    print(f"Pi Workbench vault {verb}: {vault}")
    print(f"Config: {config}")
    print("Next: open the vault in Obsidian, then use Pi with the workbench skills.")
    return 0


def cmd_raw_status(args: argparse.Namespace) -> int:
    vault = resolve_vault(args.vault)
    if vault is None:
        print("error: no Pi Workbench vault configured; run `pi-workbench setup --vault <path>`", flush=True)
        return 1
    inventory = raw_inventory(vault)
    if args.json:
        print(json.dumps(inventory, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0
    print(f"Raw inputs: {inventory['total']} ({inventory['root']})")
    for kind, count in inventory["counts"].items():
        print(f"  {kind:14} {count}")
    if inventory["uncategorized"]:
        print(f"  uncategorized  {len(inventory['uncategorized'])}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    vault = resolve_vault(args.vault)
    if vault is None:
        print("Pi Workbench doctor: fail\n- no configured vault")
        return 1
    missing = [str(path.relative_to(vault)) for path in _required_paths(vault) if not path.exists()]
    status = "pass" if not missing else "fail"
    result = {"status": status, "vault": str(vault), "missing": missing, "config": str(config_path())}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    elif missing:
        print("Pi Workbench doctor: fail")
        for relative in missing:
            print(f"- missing: {relative}")
    else:
        print("Pi Workbench doctor: pass")
        print(f"- vault: {vault}")
        print(f"- raw kinds: {', '.join(RAW_KINDS)}")
    return 0 if status == "pass" else 1


def _resolve_or_error(cli_vault: str | None) -> Path | None:
    vault = resolve_vault(cli_vault)
    if vault is None:
        print("error: no Pi Workbench vault configured; run `pi-workbench setup --vault <path>`")
        return None
    if not vault.is_dir():
        print(f"error: vault not found: {vault}")
        return None
    return vault


def cmd_query(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    try:
        scopes = parse_scopes(args.scope)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    hits = rank(vault, args.question, scopes, args.limit)
    payload = {
        "question": args.question,
        "scopes": list(scopes),
        "hits": [
            {"path": hit.page.path, "scope": hit.page.scope, "title": hit.page.title,
             "score": round(hit.score, 2), "reasons": list(hit.reasons)}
            for hit in hits
        ],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    elif not hits:
        print("No compiled pages matched. Raw inputs are excluded; run workbench-triage if the answer is still only in raw/.")
    else:
        print(f"Query: {args.question} ({', '.join(scopes)})")
        for hit in hits:
            print(f"- [{hit.page.scope}] {hit.page.path} — {hit.page.title} ({hit.score:.1f})")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    try:
        scopes = parse_scopes(args.scope)
        payload = context_pack(vault, args.topic, scopes, args.budget)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty or args.json else None))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    payload = status_snapshot(vault)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0
    raw = payload["raw"]
    print(f"Raw inputs: {raw['total']}")
    for kind, count in raw["counts"].items():
        print(f"  {kind:14} {count}")
    print(f"Compiled pages: {payload['compiled_pages']} (wiki {payload['wiki_pages']})")
    active = payload["active_projects"]
    print(f"Active projects: {len(active)}")
    for project in active:
        print(f"  - {project['title']} ({project['path']})")
    output = payload["output"]
    print(f"Output drafts: {len(output['drafts'])}")
    for draft in output["drafts"][:8]:
        print(f"  - {draft['title']} ({draft['kind']})")
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    payload = lint_report(vault)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    elif payload["status"] == "pass":
        print(f"Pi Workbench lint: pass ({payload['pages_checked']} compiled pages)")
    else:
        print(f"Pi Workbench lint: warn ({len(payload['issues'])} issue(s))")
        for issue in payload["issues"]:
            print(f"- {issue['path']}: {issue['rule']}")
    return 0 if payload["status"] == "pass" else 1


def cmd_graph(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    try:
        payload = graph_build(vault, parse_scopes(args.scope))
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    else:
        print(f"Compiled graph: {payload['stats']['pages']} pages, {payload['stats']['edges']} links")
        for node in payload["nodes"][:args.top]:
            degree = node["incoming"] + node["outgoing"]
            print(f"- {node['title']} [{node['scope']}] ({degree} links)")
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    payload = review_build(vault, raw_limit=args.raw_limit)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    else:
        print("Review prompts:")
        for prompt in payload["prompts"]:
            print(f"- {prompt}")
        print("Recent raw signals:")
        for path in payload["recent_raw"]:
            print(f"- {path}")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    path = write_dashboard(vault)
    print(path.relative_to(vault).as_posix())
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    try:
        path = capture_raw(vault, kind=args.kind, title=args.title, text=args.text, source=args.source, why=args.why)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    print(path.relative_to(vault).as_posix())
    return 0


def cmd_project(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    try:
        path = create_project(vault, slug=args.slug, title=args.title, goal=args.goal, intended_output=args.intended_output)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    print(path.relative_to(vault).as_posix())
    return 0


def cmd_output(args: argparse.Namespace) -> int:
    vault = _resolve_or_error(args.vault)
    if vault is None:
        return 1
    try:
        path = create_output(vault, kind=args.kind, slug=args.slug, title=args.title, source=args.source)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2
    print(path.relative_to(vault).as_posix())
    return 0


def cmd_install_pi_skills(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser() if args.target else Path.home() / ".pi" / "agent" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    installed = 0
    for source in sorted(
        path for path in _skills_dir().iterdir()
        if path.is_dir() and path.name.startswith("workbench-") and (path / "SKILL.md").is_file()
    ):
        destination = target / source.name
        if destination.is_symlink() or destination.is_file():
            destination.unlink()
        elif destination.is_dir():
            if (destination / "SKILL.md").exists():
                shutil.rmtree(destination)
            else:
                print(f"warning: leaving unmanaged directory untouched: {destination}")
                continue
        if args.copy:
            shutil.copytree(source, destination)
        else:
            destination.symlink_to(source, target_is_directory=True)
        installed += 1
    print(f"Installed {installed} Pi Workbench skill(s) to {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pi-agent personal workbench over an Obsidian vault.")
    parser.add_argument("-V", "--version", action="version", version=f"pi-workbench {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    setup = sub.add_parser("setup", help="create or verify a Pi Workbench vault")
    setup.add_argument("--vault", required=True, help="absolute path for the new or existing vault")
    setup.set_defaults(func=cmd_setup)

    raw = sub.add_parser("raw-status", help="show retained raw inputs by category")
    raw.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    raw.add_argument("--json", action="store_true", help="emit JSON")
    raw.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    raw.set_defaults(func=cmd_raw_status)

    query = sub.add_parser("query", help="search compiled wiki, project, and output pages")
    query.add_argument("question", help="question or key terms")
    query.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    query.add_argument("--scope", default="compiled", help="compiled | wiki | projects | output | comma-separated scopes")
    query.add_argument("--limit", type=int, default=12, help="maximum hits (default: 12)")
    query.add_argument("--json", action="store_true", help="emit JSON")
    query.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    query.set_defaults(func=cmd_query)

    context = sub.add_parser("context", help="assemble a bounded context pack from compiled pages")
    context.add_argument("topic", help="topic or task to support")
    context.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    context.add_argument("--scope", default="compiled", help="compiled | wiki | projects | output | comma-separated scopes")
    context.add_argument("--budget", type=int, default=4000, help="maximum characters (default: 4000)")
    context.add_argument("--json", action="store_true", help="emit JSON")
    context.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    context.set_defaults(func=cmd_context)

    status = sub.add_parser("status", help="show raw signals, active projects, and output drafts")
    status.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    status.add_argument("--json", action="store_true", help="emit JSON")
    status.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    status.set_defaults(func=cmd_status)

    lint = sub.add_parser("lint", help="validate compiled workbench page contracts")
    lint.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    lint.add_argument("--json", action="store_true", help="emit JSON")
    lint.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    lint.set_defaults(func=cmd_lint)

    graph = sub.add_parser("graph", help="inspect links across compiled wiki, projects, and output")
    graph.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    graph.add_argument("--scope", default="compiled", help="compiled | wiki | projects | output | comma-separated scopes")
    graph.add_argument("--top", type=int, default=10, help="maximum hub pages to print")
    graph.add_argument("--json", action="store_true", help="emit JSON")
    graph.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    graph.set_defaults(func=cmd_graph)

    review = sub.add_parser("review", help="build a non-mutating workbench review prompt")
    review.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    review.add_argument("--raw-limit", type=int, default=12, help="recent raw inputs to include")
    review.add_argument("--json", action="store_true", help="emit JSON")
    review.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    review.set_defaults(func=cmd_review)

    dashboard = sub.add_parser("dashboard", help="refresh the generated workbench dashboard")
    dashboard.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    dashboard.set_defaults(func=cmd_dashboard)

    capture = sub.add_parser("capture", help="write a minimal raw input")
    capture.add_argument("kind", choices=RAW_KINDS, help="raw category")
    capture.add_argument("title", help="short title")
    capture.add_argument("text", help="original content")
    capture.add_argument("--source", help="optional URL, author, or source locator")
    capture.add_argument("--why", help="why this may matter")
    capture.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    capture.set_defaults(func=cmd_capture)

    project = sub.add_parser("project", help="create a lightweight project work table")
    project.add_argument("slug", help="filename-safe project id")
    project.add_argument("title", help="project title")
    project.add_argument("goal", help="bounded goal")
    project.add_argument("--intended-output", default="", help="expected output path or description")
    project.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    project.set_defaults(func=cmd_project)

    output = sub.add_parser("output", help="create a draft output page")
    output.add_argument("kind", choices=OUTPUT_KINDS, help="output category")
    output.add_argument("slug", help="filename-safe output id")
    output.add_argument("title", help="output title")
    output.add_argument("--source", default="", help="optional wiki/project/output path to link as context")
    output.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    output.set_defaults(func=cmd_output)

    doctor = sub.add_parser("doctor", help="validate the workbench vault contract")
    doctor.add_argument("--vault", help="override PI_WORKBENCH_VAULT_PATH")
    doctor.add_argument("--json", action="store_true", help="emit JSON")
    doctor.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    doctor.set_defaults(func=cmd_doctor)

    install = sub.add_parser("install-pi-skills", help="install only Pi Workbench skills into Pi's skill directory")
    install.add_argument("--target", help="override the default ~/.pi/agent/skills target")
    install.add_argument("--copy", action="store_true", help="copy skills instead of symlinking")
    install.set_defaults(func=cmd_install_pi_skills)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
