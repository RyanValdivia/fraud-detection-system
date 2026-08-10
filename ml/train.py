"""Script de entrenamiento del modelo de detección de fraude.

Dataset: Sparkov Fraud Dataset (kartik2112/fraud-detection en Kaggle)
https://www.kaggle.com/datasets/kartik2112/fraud-detection

Descargar `fraudTrain.csv` en `data/` (ver data/README.md) y correr:

    python ml/train.py

Genera las mismas features que `app/features.py` calcula en serving
(mismo orden y significado, ver `app/constants.py::FEATURE_NAMES`),
entrena XGBoost / LightGBM / RandomForest, elige el mejor por average
precision (métrica correcta dado el fuerte desbalance fraude/no-fraude)
y lo guarda en `ml/models/model.pkl`.
"""

import os
import sys

import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.constants import CATEGORIES, FEATURE_NAMES  # noqa: E402
from app.geo import age_from_dob, haversine_km  # noqa: E402

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MODEL_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "models", "model.pkl")


def load_raw(filename: str = "fraudTrain.csv") -> pd.DataFrame:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No se encontró {path}. Descarga el dataset (ver data/README.md) "
            f"y coloca '{filename}' en data/."
        )
    return pd.read_csv(path)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Genera FEATURE_NAMES a partir de las columnas crudas del dataset Sparkov.

    Debe producir exactamente las mismas columnas (mismo orden, mismo
    significado) que `app/features.py::build_feature_vector` calcula en
    serving, salvo `velocity_1h`, que aquí se aproxima offline contando
    transacciones previas de la misma tarjeta en la última hora (en
    producción ese conteo lo lleva Redis).
    """
    df = df.copy()
    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"])
    df["dob"] = pd.to_datetime(df["dob"])

    df["hour"] = df["trans_date_trans_time"].dt.hour
    df["is_night"] = ((df["hour"] < 6) | (df["hour"] > 22)).astype(int)

    df["category_idx"] = df["category"].apply(
        lambda c: CATEGORIES.index(c) if c in CATEGORIES else len(CATEGORIES)
    )
    df["gender_idx"] = (df["gender"] == "M").astype(int)

    df["age"] = df.apply(
        lambda r: age_from_dob(r["dob"].date(), r["trans_date_trans_time"]), axis=1
    )
    df["distance_km"] = df.apply(
        lambda r: haversine_km(r["lat"], r["long"], r["merch_lat"], r["merch_long"]),
        axis=1,
    )

    # velocity_1h: transacciones previas de la misma tarjeta en la última hora
    # (equivalente offline al contador de Redis en app/features.py)
    df = df.sort_values(["cc_num", "trans_date_trans_time"])
    df = df.set_index("trans_date_trans_time")
    df["velocity_1h"] = (
        df.groupby("cc_num")["amt"]
        .rolling("1h")
        .count()
        .reset_index(level=0, drop=True)
    )
    df = df.reset_index()

    return df[FEATURE_NAMES + ["is_fraud"]]


def evaluate(name, model, X_test, y_test) -> float:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    ap = average_precision_score(y_test, y_proba)
    print(f"\n=== {name} (average precision = {ap:.4f}) ===")
    print(classification_report(y_test, y_pred, digits=4))
    return ap


def train():
    raw = load_raw()
    print(f"Dataset cargado: {len(raw)} filas")

    featured = build_features(raw)
    X = featured[FEATURE_NAMES]
    y = featured["is_fraud"]
    print(f"Tasa de fraude: {y.mean():.4%} ({y.sum()} / {len(y)})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    scale_pos_weight = (y_train == 0).sum() / max((y_train == 1).sum(), 1)

    candidates = {
        "XGBoost": XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.1,
            eval_metric="aucpr",
            scale_pos_weight=scale_pos_weight,
            random_state=42,
        ),
        "LightGBM": LGBMClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.1,
            class_weight="balanced",
            random_state=42,
            verbosity=-1,
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    }

    results = {}
    best_name, best_model, best_ap = None, None, -1
    for name, model in candidates.items():
        model.fit(X_train, y_train)
        ap = evaluate(name, model, X_test, y_test)
        results[name] = ap
        if ap > best_ap:
            best_name, best_model, best_ap = name, model, ap

    print(f"\nMejor modelo: {best_name} (average precision = {best_ap:.4f})")

    os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
    joblib.dump(best_model, MODEL_OUTPUT_PATH)
    print(f"Modelo guardado en {MODEL_OUTPUT_PATH}")

    return results, best_name


if __name__ == "__main__":
    train()
