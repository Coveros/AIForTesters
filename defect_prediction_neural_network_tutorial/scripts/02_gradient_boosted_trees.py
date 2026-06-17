#!/usr/bin/env python3
"""Step 2: Gradient boosted trees baseline (sklearn, no extra installs)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
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

    x = train_df[features].to_numpy()
    y = train_df[config.data.label_column].to_numpy(dtype=int)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.training.val_split, random_state=config.training.seed
    )

    pos = float(np.sum(y_train == 1))
    neg = float(np.sum(y_train == 0))
    sample_weight = np.where(y_train == 1, neg / pos, 1.0) if pos else None

    model = HistGradientBoostingClassifier(
        max_iter=config.boosting.n_estimators,
        learning_rate=config.boosting.learning_rate,
        max_depth=config.boosting.max_depth,
        random_state=config.training.seed,
        early_stopping=True,
        n_iter_no_change=config.boosting.early_stopping_rounds,
    )
    model.fit(x_train, y_train, sample_weight=sample_weight)
    auc = roc_auc_score(y_test, model.predict_proba(x_test)[:, 1])

    print("Step 2: Gradient Boosted Trees")
    print(f"  Features: {features}")
    print(f"  AUC-ROC:  {auc:.4f}")

    out = CHECKPOINT_DIR / "02_gradient_boosted_trees.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"features": features, "auc_roc": auc}, f, indent=2)
    print(f"  Saved:    {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
