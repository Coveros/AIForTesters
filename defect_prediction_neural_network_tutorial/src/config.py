from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class DataConfig:
    train_path: str = "data/raw/jm1.csv"
    val_path: str | None = "data/raw/cm1.csv"
    label_column: str = "defects"
    feature_columns: list[str] | None = None
    base_features: list[str] | None = None
    variant_feature: str = "i"
    normalize: bool = True
    preprocessing: str = "nasa"  # nasa | none
    split_mode: str = "external"  # external | random


@dataclass
class ModelConfig:
    input_dim: int = 1536
    hidden_dims: list[int] = field(default_factory=lambda: [7168, 7168, 3584, 1024])
    dropout: float = 0.2
    num_classes: int = 1


@dataclass
class TrainingConfig:
    epochs: int = 20
    batch_size: int = 64
    learning_rate: float = 1e-4
    weight_decay: float = 1e-5
    val_split: float = 0.2
    seed: int = 42
    num_workers: int = 0
    checkpoint_dir: str = "checkpoints"
    save_best: bool = True


@dataclass
class HardwareConfig:
    device: str = "auto"


@dataclass
class BoostingConfig:
    n_estimators: int = 500
    learning_rate: float = 0.05
    max_depth: int = 6
    early_stopping_rounds: int = 50


@dataclass
class Config:
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    hardware: HardwareConfig = field(default_factory=HardwareConfig)
    boosting: BoostingConfig = field(default_factory=BoostingConfig)


def _merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _merge_dict(merged[key], value)
        else:
            merged[key] = value
    return merged


def _section(data: dict[str, Any], cls: type):
    return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def load_config(path: str | Path) -> Config:
    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    return Config(
        data=_section(raw.get("data", {}), DataConfig),
        model=_section(raw.get("model", {}), ModelConfig),
        training=_section(raw.get("training", {}), TrainingConfig),
        hardware=_section(raw.get("hardware", {}), HardwareConfig),
        boosting=_section(raw.get("boosting", {}), BoostingConfig),
    )
