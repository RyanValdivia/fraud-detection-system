"""Carga del modelo entrenado y lógica de predicción/decisión."""

import os

import joblib
import numpy as np

from app.config import settings


class FraudModel:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self._load()

    def _load(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            self.model = None  # sin modelo entrenado aún

    def predict_proba(self, features: np.ndarray) -> float:
        if self.model is None:
            # fallback determinista mientras no exista un modelo entrenado
            return 0.0
        proba = self.model.predict_proba(features)[0][1]
        return float(proba)

    @staticmethod
    def decide(probability: float) -> str:
        if probability >= settings.fraud_block_threshold:
            return "block"
        if probability >= settings.fraud_review_threshold:
            return "review"
        return "allow"


fraud_model = FraudModel(settings.model_path)
