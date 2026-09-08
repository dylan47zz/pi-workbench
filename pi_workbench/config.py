"""Independent configuration for Pi Workbench.

The fork deliberately does not reuse obsidian-wiki's global config path: a
person can operate an upstream wiki and a Pi Workbench vault side by side.
"""

from __future__ import annotations

import os
from pathlib import Path

HOME = Path.home()


def config_dir() -> Path:
    override = os.environ.get("PI_WORKBENCH_CONFIG_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    xdg_home = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg_home).expanduser() if xdg_home else HOME / ".config"
    return base / "pi-workbench"


def config_path() -> Path:
    return config_dir() / "config"


def read_config() -> dict[str, str]:
    path = config_path()
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def resolve_vault(cli_vault: str | None = None) -> Path | None:
    if cli_vault:
        return Path(cli_vault).expanduser().resolve()
    configured = read_config().get("PI_WORKBENCH_VAULT_PATH", "").strip()
    return Path(configured).expanduser().resolve() if configured else None


def write_config(vault: Path, version: str) -> Path:
    """Write only Pi Workbench-owned keys, preserving user comments and settings."""
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    owned = {
        "PI_WORKBENCH_VAULT_PATH": str(vault.resolve()),
        "PI_WORKBENCH_VERSION": version,
    }
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    out: list[str] = []
    seen: set[str] = set()
    for raw in existing:
        stripped = raw.strip()
        key = stripped.split("=", 1)[0].strip() if "=" in stripped else ""
        if key in owned and not stripped.startswith("#"):
            if key not in seen:
                out.append(f'{key}="{owned[key]}"')
                seen.add(key)
            continue
        out.append(raw)
    for key, value in owned.items():
        if key not in seen:
            out.append(f'{key}="{value}"')
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path
