from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class Config:
    experiment_name: str
    random_state: int
    train: dict[str, Any]
    model: dict[str, Any]
    monitoring: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        return cls(
            experiment_name=data["experiment_name"],
            random_state=data.get("random_state", 42),
            train=data["train"],
            model=data["model"],
            monitoring=data.get("monitoring", {}),
        )


def load_config(path: Path) -> Config:
    with path.open("r", encoding="utf-8") as fp:
        raw = yaml.safe_load(fp)
    return Config.from_dict(raw)


def load_dataset(config: Config) -> pd.DataFrame:
    csv_path = Path(config.train["input_path"])
    if csv_path.exists():
        return pd.read_csv(csv_path, parse_dates=[config.train["date_column"]])

    # Generate synthetic dataset for initial development
    n_samples = 1000
    rng = np.random.default_rng(seed=config.random_state)

    df = pd.DataFrame(
        {
            "patient_age_band": rng.choice(["18-29", "30-44", "45-64", "65+"], size=n_samples),
            "visit_type": rng.choice(["primary_care", "behavioral", "telehealth", "specialist"], size=n_samples),
            "provider_specialty": rng.choice(["pediatrics", "cardiology", "dermatology"], size=n_samples),
            "channel": rng.choice(["mobile", "web", "phone"], size=n_samples, p=[0.5, 0.3, 0.2]),
            "insurance_plan": rng.choice(["commercial", "medicare", "medicaid", "self-pay"], size=n_samples),
            "lead_time_days": rng.integers(0, 30, size=n_samples),
            "distance_miles": rng.normal(7, 3, size=n_samples).clip(min=0),
            "prior_no_show_rate": rng.uniform(0, 0.8, size=n_samples),
            "prior_cancellations": rng.poisson(1.5, size=n_samples),
            "appointment_start": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 120, size=n_samples), unit="D"),
        }
    )
    logits = (
        -2
        + 0.03 * df["lead_time_days"]
        + 0.4 * df["prior_no_show_rate"]
        + 0.2 * (df["channel"] == "web").astype(int)
        + 0.1 * (df["distance_miles"] > 10).astype(int)
    )
    probabilities = 1 / (1 + np.exp(-logits))
    df["no_show"] = rng.binomial(1, probabilities)
    return df


def build_pipeline(config: Config) -> Pipeline:
    categorical_features = config.train["categorical_features"]
    numeric_features = config.train["numeric_features"]

    transformers = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("numeric", Pipeline(steps=[("scaler", StandardScaler())]), numeric_features),
        ]
    )

    model_type = config.model.get("type", "gradient_boosting")
    if model_type != "gradient_boosting":
        raise NotImplementedError(f"Model type '{model_type}' not supported yet.")

    classifier = GradientBoostingClassifier(random_state=config.random_state, **config.model.get("params", {}))
    pipeline = Pipeline(
        steps=[
            ("transformers", transformers),
            ("classifier", classifier),
        ]
    )
    return pipeline


def train_and_evaluate(config: Config) -> dict[str, Any]:
    df = load_dataset(config)
    target_col = config.train["target_column"]

    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=config.train["test_size"],
        random_state=config.random_state,
        stratify=y,
    )
    val_size = config.train.get("validation_size", 0.1)
    val_ratio = val_size / (1 - config.train["test_size"])
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=1 - val_ratio,
        random_state=config.random_state,
        stratify=y_temp,
    )

    pipeline = build_pipeline(config)
    pipeline.fit(X_train, y_train)

    y_val_pred = pipeline.predict_proba(X_val)[:, 1]
    y_test_pred = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "val_roc_auc": roc_auc_score(y_val, y_val_pred),
        "test_roc_auc": roc_auc_score(y_test, y_test_pred),
        "classification_report": classification_report(y_test, (y_test_pred > 0.5).astype(int), output_dict=True),
    }

    artifacts_dir = Path("models") / f"{config.experiment_name}"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = artifacts_dir / "metrics.json"
    with metrics_path.open("w", encoding="utf-8") as fp:
        json.dump(metrics, fp, indent=2)

    model_path = artifacts_dir / "pipeline.pkl"
    pd.to_pickle(pipeline, model_path)

    return {
        "metrics_path": str(metrics_path),
        "model_path": str(model_path),
        "metrics": metrics,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the CareFlow AI no-show risk model.")
    parser.add_argument("--config", type=str, default="config.yml", help="Path to YAML configuration file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(Path(args.config))
    result = train_and_evaluate(config)
    print(json.dumps({"status": "completed", **result}, indent=2))


if __name__ == "__main__":
    main()
