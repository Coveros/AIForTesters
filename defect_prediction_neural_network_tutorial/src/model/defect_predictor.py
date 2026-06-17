from __future__ import annotations

import torch
import torch.nn as nn

from src.config import ModelConfig


class DefectPredictor(nn.Module):
    """MLP for binary defect prediction."""

    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config

        layers: list[nn.Module] = []
        in_dim = config.input_dim

        for hidden_dim in config.hidden_dims:
            layers.extend(
                [
                    nn.Linear(in_dim, hidden_dim),
                    nn.BatchNorm1d(hidden_dim),
                    nn.GELU(),
                    nn.Dropout(config.dropout),
                ]
            )
            in_dim = hidden_dim

        layers.append(nn.Linear(in_dim, config.num_classes))
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def build_model(config: ModelConfig) -> DefectPredictor:
    return DefectPredictor(config)
