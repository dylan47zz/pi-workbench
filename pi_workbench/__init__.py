"""Pi Workbench: a Pi-agent operating layer over an Obsidian knowledge vault."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pi-workbench")
except PackageNotFoundError:  # running from a source tree without an install
    __version__ = "0.0.0+dev"

__all__ = ["__version__"]
