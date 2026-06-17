from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from torch.utils.data import DataLoader
from src.config import Config
from src.paths import resolve_path
from src.model.defect_predictor import DefectPredictor, count_parameters


def resolve_device(preference: str) -> torch.device:
    if preference == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        if torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    return torch.device(preference)


class Trainer:
    def __init__(
        self,
        model: DefectPredictor,
        config: Config,
        train_loader: DataLoader,
        val_loader: DataLoader,
    ):
        self.model = model
        self.config = config
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = resolve_device(config.hardware.device)
        self.model.to(self.device)

        self.criterion = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=config.training.learning_rate,
            weight_decay=config.training.weight_decay,
        )

        self.checkpoint_dir = resolve_path(config.training.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.history: list[dict[str, float]] = []
        self.best_val_loss = float("inf")

    def _run_epoch(self, loader: DataLoader, train: bool) -> tuple[float, dict[str, float]]:
        self.model.train(train)
        total_loss = 0.0
        all_probs: list[float] = []
        all_labels: list[float] = []

        context = torch.enable_grad() if train else torch.no_grad()
        with context:
            for features, labels in loader:
                features = features.to(self.device)
                labels = labels.to(self.device)

                logits = self.model(features)
                loss = self.criterion(logits, labels)

                if train:
                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()

                total_loss += loss.item() * features.size(0)
                probs = torch.sigmoid(logits).detach().cpu().numpy().ravel()
                all_probs.extend(probs.tolist())
                all_labels.extend(labels.detach().cpu().numpy().ravel().tolist())

        avg_loss = total_loss / len(loader.dataset)
        preds = [1 if p >= 0.5 else 0 for p in all_probs]
        metrics = {
            "accuracy": float(accuracy_score(all_labels, preds)),
            "precision": float(precision_score(all_labels, preds, zero_division=0)),
            "recall": float(recall_score(all_labels, preds, zero_division=0)),
            "f1": float(f1_score(all_labels, preds, zero_division=0)),
        }

        if len(set(all_labels)) > 1:
            metrics["roc_auc"] = float(roc_auc_score(all_labels, all_probs))
        else:
            metrics["roc_auc"] = float("nan")

        return avg_loss, metrics

    def train(self) -> list[dict[str, float]]:
        param_count = count_parameters(self.model)
        print(f"Model parameters: {param_count:,}")
        print(f"Training on {self.device} for {self.config.training.epochs} epochs")

        for epoch in range(1, self.config.training.epochs + 1):
            train_loss, train_metrics = self._run_epoch(self.train_loader, train=True)
            val_loss, val_metrics = self._run_epoch(self.val_loader, train=False)

            record = {
                "epoch": epoch,
                "train_loss": train_loss,
                "val_loss": val_loss,
                **{f"train_{k}": v for k, v in train_metrics.items()},
                **{f"val_{k}": v for k, v in val_metrics.items()},
            }
            self.history.append(record)

            print(
                f"Epoch {epoch:02d}/{self.config.training.epochs} | "
                f"train_loss={train_loss:.4f} val_loss={val_loss:.4f} | "
                f"val_f1={val_metrics['f1']:.4f} val_auc={val_metrics['roc_auc']:.4f}"
            )

            if self.config.training.save_best and val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self._save_checkpoint("best.pt", record)

        self._save_checkpoint("last.pt", self.history[-1])
        self._save_history()
        return self.history

    def _save_checkpoint(self, filename: str, metrics: dict) -> None:
        path = self.checkpoint_dir / filename
        torch.save(
            {
                "model_state_dict": self.model.state_dict(),
                "config": asdict(self.config),
                "metrics": metrics,
            },
            path,
        )

    def _save_history(self) -> None:
        history_path = self.checkpoint_dir / "history.json"
        with open(history_path, "w") as f:
            json.dump(self.history, f, indent=2)
