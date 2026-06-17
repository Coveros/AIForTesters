#!/usr/bin/env python3
"""Download NASA PROMISE JM1 and CM1 datasets."""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.paths import CM1_PATH, DATA_DIR, JM1_PATH

DATASETS = {
    JM1_PATH: (
        "https://raw.githubusercontent.com/ApoorvaKrisna/"
        "NASA-promise-dataset-repository/main/jm1.csv"
    ),
    CM1_PATH: (
        "https://raw.githubusercontent.com/ApoorvaKrisna/"
        "NASA-promise-dataset-repository/main/cm1.csv"
    ),
}


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for dest, url in DATASETS.items():
        print(f"Downloading {dest.name} ...")
        urlretrieve(url, dest)
        print(f"  -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
