from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset

from src.config import Config
from src.paths import resolve_path
from src.data.nasa_preprocessing import (
    NASA_DEFAULT_FEATURES,
    NASA_DEFAULT_VARIANT_FEATURE,
    build_feature_columns,
    load_nasa_dataset,
    variant_feature_options,
)


class DefectDataset(Dataset):
    def __init__(self, features: np.ndarray, labels: np.ndarray):
        self.features = torch.as_tensor(features, dtype=torch.float32)
        self.labels = torch.as_tensor(labels, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.features[idx], self.labels[idx]


def _read_csv(path: Path, config: Config) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    if config.data.preprocessing == "nasa":
        return load_nasa_dataset(str(path))
    return pd.read_csv(path)


def _extract_xy(
    df: pd.DataFrame,
    label_column: str,
    feature_columns: list[str] | None,
) -> tuple[np.ndarray, np.ndarray]:
    if label_column not in df.columns:
        raise ValueError(f"Label column '{label_column}' not found in dataset")

    if feature_columns is None:
        feature_columns = [c for c in df.columns if c != label_column]

    missing = [c for c in feature_columns if c not in df.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    x = df[feature_columns].to_numpy(dtype=np.float32)
    y = df[label_column].to_numpy(dtype=np.float32)

    if y.ndim == 1:
        y = y.reshape(-1, 1)

    return x, y


def resolve_feature_columns(config: Config) -> list[str]:
    if config.data.feature_columns:
        return list(config.data.feature_columns)
    if config.data.preprocessing == "nasa":
        return build_feature_columns(
            base_features=config.data.base_features,
            variant_feature=config.data.variant_feature,
        )
    return []


def load_splits(
    config: Config,
) -> tuple[DefectDataset, DefectDataset, StandardScaler | None, list[str]]:
    feature_columns = resolve_feature_columns(config)
    train_df = _read_csv(resolve_path(config.data.train_path), config)
    val_path = resolve_path(config.data.val_path) if config.data.val_path else None

    if config.data.split_mode == "external" and val_path and val_path.exists():
        val_df = _read_csv(val_path, config)
        x_train, y_train = _extract_xy(train_df, config.data.label_column, feature_columns)
        x_val, y_val = _extract_xy(val_df, config.data.label_column, feature_columns)
    else:
        x_all, y_all = _extract_xy(train_df, config.data.label_column, feature_columns)
        x_train, x_val, y_train, y_val = train_test_split(
            x_all,
            y_all,
            test_size=config.training.val_split,
            random_state=config.training.seed,
            stratify=y_all if len(np.unique(y_all)) > 1 else None,
        )

    if not feature_columns:
        feature_columns = [
            c for c in train_df.columns if c != config.data.label_column
        ]

    scaler: StandardScaler | None = None
    if config.data.normalize:
        scaler = StandardScaler()
        x_train = scaler.fit_transform(x_train).astype(np.float32)
        x_val = scaler.transform(x_val).astype(np.float32)

    return (
        DefectDataset(x_train, y_train),
        DefectDataset(x_val, y_val),
        scaler,
        feature_columns,
    )


def build_dataloader(dataset: DefectDataset, config: Config, shuffle: bool) -> DataLoader:
    return DataLoader(
        dataset,
        batch_size=config.training.batch_size,
        shuffle=shuffle,
        num_workers=config.training.num_workers,
        pin_memory=False,
    )
