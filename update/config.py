import os
from pathlib import Path


def find_repo_root(start_dir: Path | None = None) -> Path:
    """Find repository root by searching upwards for pyproject.toml or .git.

    Fallback to the package source root if neither marker is found.
    """
    current = (start_dir or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    return Path(__file__).resolve().parent.parent


# Base repository directory resolved dynamically
ROOT_DIR = find_repo_root()

# Configurable paths with environment variable override support
PATH = Path(os.getenv("README_INFO_DIR", ROOT_DIR / "readme_info"))
SUBMOD = Path(os.getenv("WEBSITE_DIR", ROOT_DIR / "kevinfjiang.github.io"))
