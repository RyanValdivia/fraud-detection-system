"""Feature engineering para el modelo de detección de fraude.

Convierte una transacción cruda en un vector de features numérico
que el modelo entrenado espera recibir.
"""

import numpy as np

from app.cache import redis_client
from app.schemas import TransactionRequest

MERCHANT_CATEGORIES = [
    "grocery", "electronics", "travel", "entertainment",
    "fashion", "gambling", "crypto", "other",
]


def _merchant_category_index(category: str) -> int:
    category = category.lower()
    return MERCHANT_CATEGORIES.index(category) if category in MERCHANT_CATEGORIES else len(MERCHANT_CATEGORIES)


def _user_velocity(user_id: str) -> int:
    """Cuenta transacciones recientes del usuario usando Redis como feature store rápido."""
    key = f"velocity:{user_id}"
    count = redis_client.incr(key)
    redis_client.expire(key, 3600)  # ventana de 1 hora
    return count


def build_feature_vector(tx: TransactionRequest) -> np.ndarray:
    hour = tx.timestamp.hour
    is_night = 1 if hour < 6 or hour > 22 else 0
    velocity_1h = _user_velocity(tx.user_id)

    features = [
        tx.amount,
        hour,
        is_night,
        _merchant_category_index(tx.merchant_category),
        velocity_1h,
        1 if tx.device_id is None else 0,
    ]
    return np.array(features, dtype=float).reshape(1, -1)
