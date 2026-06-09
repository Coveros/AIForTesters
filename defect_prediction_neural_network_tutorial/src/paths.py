"""Project-root paths that work no matter where a script is run from."""

from __future__ import annotations

from pathlib import Path

# Repo root: parent of src/
ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT / "data" / "raw"
CONFIG_PATH = ROOT / "config" / "default.yaml"
CHECKPOINT_DIR = ROOT / "checkpoints"

JM1_PATH = DATA_DIR / "jm1.csv"
CM1_PATH = DATA_DIR / "cm1.csv"


def resolve_path(path: str | Path) -> Path:
    """Turn a config-relative path into an absolute path under ROOT."""
    p = Path(path)
    return p if p.is_absolute() else ROOT / p
