#!/usr/bin/env python3
"""Step 1: Logistic regression baseline (matches defect_prediction.ipynb)."""

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
from src.data.dataset import resolve_feature_columns
from src.data.nasa_preprocessing import load_nasa_dataset
from src.paths import CHECKPOINT_DIR, CONFIG_PATH, resolve_path


def main() -> None:
    config = load_config(CONFIG_PATH)
    train_df = load_nasa_dataset(resolve_path(config.data.train_path))
    features = resolve_feature_columns(config)

    x = train_df[features]
    y = train_df[config.data.label_column].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.training.val_split, random_state=config.training.seed
    )

    model = LogisticRegression(random_state=config.training.seed, max_iter=1000)
    model.fit(x_train, y_train)
    auc = roc_auc_score(y_test, model.predict_proba(x_test)[:, 1])

    print("Step 1: Logistic Regression")
    print(f"  Features: {features}")
    print(f"  AUC-ROC:  {auc:.4f}  (~0.727 with default features)")

    out = CHECKPOINT_DIR / "01_logistic_regression.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"features": features, "auc_roc": auc}, f, indent=2)
    print(f"  Saved:    {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
