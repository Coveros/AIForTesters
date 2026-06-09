#!/usr/bin/env python3
"""Step 3: Try each candidate for the 6th feature and pick the best."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import load_config
from src.data.nasa_preprocessing import (
    NASA_BASE_FEATURES,
    build_feature_columns,
    load_nasa_dataset,
    variant_feature_options,
)
from src.paths import CHECKPOINT_DIR, CONFIG_PATH, resolve_path


def main() -> None:
    config = load_config(CONFIG_PATH)
    train_df = load_nasa_dataset(resolve_path(config.data.train_path))
    base = list(config.data.base_features or NASA_BASE_FEATURES)

    print("Step 3: Compare 6th Feature Candidates")
    print(f"  Fixed features: {base}\n")
    print(f"{'Rank':<5} {'Feature':<16} {'AUC-ROC':>8}")
    print("-" * 32)

    results = []
    for variant in variant_feature_options(base):
        features = build_feature_columns(base, variant)
        x = train_df[features]
        y = train_df[config.data.label_column].astype(int)

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=config.training.val_split, random_state=config.training.seed
        )
        model = LogisticRegression(random_state=config.training.seed, max_iter=1000)
        model.fit(x_train, y_train)
        auc = roc_auc_score(y_test, model.predict_proba(x_test)[:, 1])
        results.append({"variant_feature": variant, "features": features, "auc_roc": auc})

    results.sort(key=lambda r: r["auc_roc"], reverse=True)
    for rank, row in enumerate(results, start=1):
        mark = " <-- best" if rank == 1 else ""
        print(f"{rank:<5} {row['variant_feature']:<16} {row['auc_roc']:>8.4f}{mark}")

    best = results[0]
    print(f"\n  Update config/default.yaml:")
    print(f"    variant_feature: {best['variant_feature']}")
    print(f"  Then run Step 4.")

    out = CHECKPOINT_DIR / "03_feature_comparison.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"base_features": base, "results": results, "best": best}, f, indent=2)
    print(f"  Saved: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
