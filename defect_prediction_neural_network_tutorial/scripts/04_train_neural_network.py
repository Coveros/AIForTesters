#!/usr/bin/env python3
"""Step 4: Train the neural network on JM1 and evaluate on CM1."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.config import load_config
from src.data.dataset import build_dataloader, load_splits
from src.model.defect_predictor import DefectPredictor, count_parameters
from src.paths import CONFIG_PATH, resolve_path
from src.training.trainer import Trainer


def main() -> None:
    config = load_config(CONFIG_PATH)
    train_ds, val_ds, scaler, features = load_splits(config)

    config.model.input_dim = len(features)
    model = DefectPredictor(config.model)

    print("Step 4: Neural Network")
    print(f"  Features:   {features}")
    print(f"  Parameters: {count_parameters(model):,}")
    print(f"  Train:      {config.data.train_path}")
    print(f"  Evaluate:   {config.data.val_path}")
    print()

    trainer = Trainer(
        model,
        config,
        build_dataloader(train_ds, config, True),
        build_dataloader(val_ds, config, False),
    )
    history = trainer.train()

    best = max(history, key=lambda e: e.get("val_roc_auc", 0))
    print(f"\n  Best val AUC: {best['val_roc_auc']:.4f} (epoch {best['epoch']})")

    if scaler is not None:
        path = resolve_path(config.training.checkpoint_dir) / "scaler.pkl"
        with open(path, "wb") as f:
            pickle.dump(scaler, f)


if __name__ == "__main__":
    main()
