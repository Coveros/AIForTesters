from __future__ import annotations

import pandas as pd

# All software metrics available in the NASA PROMISE JM1/CM1 datasets.
NASA_ALL_FEATURES: list[str] = [
    "loc",
    "v(g)",
    "ev(g)",
    "iv(g)",
    "n",
    "v",
    "l",
    "d",
    "i",
    "e",
    "b",
    "t",
    "lOCode",
    "lOComment",
    "lOBlank",
    "locCodeAndComment",
    "uniq_Op",
    "uniq_Opnd",
    "total_Op",
    "total_Opnd",
    "branchCount",
]

# Default feature subset from defect_prediction.ipynb (Step 3).
NASA_BASE_FEATURES: list[str] = [
    "loc",
    "d",
    "locCodeAndComment",
    "v(g)",
    "uniq_Opnd",
]

NASA_DEFAULT_VARIANT_FEATURE: str = "i"

NASA_DEFAULT_FEATURES: list[str] = NASA_BASE_FEATURES + [NASA_DEFAULT_VARIANT_FEATURE]


def build_feature_columns(
    base_features: list[str] | None = None,
    variant_feature: str = NASA_DEFAULT_VARIANT_FEATURE,
) -> list[str]:
    """Build the 6-feature set: 5 fixed metrics + one swappable metric."""
    base = list(base_features or NASA_BASE_FEATURES)
    if variant_feature in base:
        raise ValueError(
            f"variant_feature '{variant_feature}' is already in base_features: {base}"
        )
    if variant_feature not in NASA_ALL_FEATURES:
        raise ValueError(
            f"Unknown variant_feature '{variant_feature}'. "
            f"Choose from: {NASA_ALL_FEATURES}"
        )
    return base + [variant_feature]


def variant_feature_options(
    base_features: list[str] | None = None,
) -> list[str]:
    """Metrics available for the 6th feature slot (excludes base features)."""
    base = set(base_features or NASA_BASE_FEATURES)
    return [name for name in NASA_ALL_FEATURES if name not in base]


def preprocess_nasa_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the cleaning steps from defect_prediction.ipynb."""
    cleaned = df.copy()
    cleaned.replace("?", pd.NA, inplace=True)
    cleaned.dropna(subset=cleaned.columns[4:6], inplace=True)

    numeric_cols = cleaned.columns[16:21]
    cleaned[numeric_cols] = cleaned[numeric_cols].apply(pd.to_numeric, errors="coerce")
    cleaned.dropna(inplace=True)
    cleaned[numeric_cols] = cleaned[numeric_cols].astype(int)

    if cleaned["defects"].dtype == object:
        cleaned["defects"] = (
            cleaned["defects"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"false": 0, "true": 1})
        )
    else:
        cleaned["defects"] = cleaned["defects"].astype(int)

    cleaned.dropna(subset=["defects"], inplace=True)
    cleaned["defects"] = cleaned["defects"].astype(int)
    return cleaned.reset_index(drop=True)


def load_nasa_dataset(path: str) -> pd.DataFrame:
    return preprocess_nasa_dataframe(pd.read_csv(path))
