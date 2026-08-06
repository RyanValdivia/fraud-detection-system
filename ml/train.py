"""Script de entrenamiento del modelo de detección de fraude.

Uso:
    python ml/train.py

Por defecto genera datos sintéticos de ejemplo. Reemplazar `load_dataset()`
por la carga de un dataset real (ej. Kaggle Credit Card Fraud Detection).
"""

import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

MODEL_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "models", "model.pkl")


def load_dataset(n_samples: int = 5000, random_state: int = 42) -> pd.DataFrame:
    """Genera un dataset sintético con las mismas features que app/features.py."""
    rng = np.random.default_rng(random_state)

    amount = rng.exponential(scale=80, size=n_samples)
    hour = rng.integers(0, 24, size=n_samples)
    is_night = ((hour < 6) | (hour > 22)).astype(int)
    merchant_category = rng.integers(0, 8, size=n_samples)
    velocity_1h = rng.poisson(lam=1.5, size=n_samples)
    no_device = rng.integers(0, 2, size=n_samples)

    fraud_score = (
        0.02 * amount
        + 2.0 * is_night
        + 1.5 * (merchant_category == 6)  # crypto
        + 1.2 * velocity_1h
        + 1.0 * no_device
        + rng.normal(0, 1, size=n_samples)
    )
    threshold = np.percentile(fraud_score, 95)
    is_fraud = (fraud_score > threshold).astype(int)

    return pd.DataFrame({
        "amount": amount,
        "hour": hour,
        "is_night": is_night,
        "merchant_category": merchant_category,
        "velocity_1h": velocity_1h,
        "no_device": no_device,
        "is_fraud": is_fraud,
    })


def train():
    df = load_dataset()
    X = df.drop(columns=["is_fraud"])
    y = df["is_fraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    joblib.dump(model, MODEL_OUTPUT_PATH)
    print(f"Modelo guardado en {MODEL_OUTPUT_PATH}")


if __name__ == "__main__":
    train()
