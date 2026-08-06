"""Script de entrenamiento del modelo de detección de fraude.

Dataset: Sparkov Fraud Dataset (kartik2112/fraud-detection en Kaggle)
https://www.kaggle.com/datasets/kartik2112/fraud-detection

Descargar `fraudTrain.csv` en `data/` (ver data/README.md) y correr:

    python ml/train.py

ESTADO: scaffold. Falta implementar:
  - [ ] feature engineering (usar app/constants.py + app/geo.py como base:
        category_idx, gender_idx, age, distance_km, hour, is_night,
        city_pop, velocity_1h)
  - [ ] split train/test
  - [ ] entrenar y comparar XGBoost / LightGBM / RandomForest
  - [ ] elegir mejor por average precision (dataset muy desbalanceado)
  - [ ] guardar el mejor modelo en ml/models/model.pkl
"""

import os

import pandas as pd

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
    """TODO: aplicar app.geo.haversine_km / age_from_dob y app.constants.CATEGORIES
    para generar las mismas columnas que app/features.py calcula en serving."""
    raise NotImplementedError


def train():
    df = load_raw()
    print(f"Dataset cargado: {len(df)} filas, columnas: {list(df.columns)}")
    # TODO: build_features(df) -> X, y
    # TODO: train_test_split
    # TODO: entrenar XGBoost / LightGBM / RandomForest y comparar
    # TODO: joblib.dump(best_model, MODEL_OUTPUT_PATH)
    raise NotImplementedError("Entrenamiento aún no implementado")


if __name__ == "__main__":
    train()
