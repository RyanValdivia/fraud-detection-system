"""Feature engineering para el modelo de detección de fraude.

Convierte una transacción cruda en el mismo vector de features que
ml/train.py genera a partir del dataset (deben coincidir orden y
significado: ver app/constants.py -> FEATURE_NAMES).
"""

import numpy as np

from app.cache import redis_client
from app.constants import CATEGORIES
from app.geo import age_from_dob, haversine_km
from app.schemas import TransactionRequest


def _category_index(category: str) -> int:
    category = category.lower()
    return CATEGORIES.index(category) if category in CATEGORIES else len(CATEGORIES)


def _gender_index(gender: str) -> int:
    return 1 if gender.upper() == "M" else 0


def _user_velocity(cc_num: str) -> int:
    """Cuenta transacciones recientes de la tarjeta usando Redis como feature store rápido."""
    key = f"velocity:{cc_num}"
    count = redis_client.incr(key)
    redis_client.expire(key, 3600)  # ventana de 1 hora
    return count


def build_feature_vector(tx: TransactionRequest) -> tuple[np.ndarray, float]:
    hour = tx.trans_time.hour
    is_night = 1 if hour < 6 or hour > 22 else 0
    age = age_from_dob(tx.dob, tx.trans_time)
    distance_km = haversine_km(tx.lat, tx.long, tx.merch_lat, tx.merch_long)
    velocity_1h = _user_velocity(tx.cc_num)

    features = [
        tx.amt,
        _category_index(tx.category),
        _gender_index(tx.gender),
        age,
        distance_km,
        hour,
        is_night,
        tx.city_pop,
        velocity_1h,
    ]
    return np.array(features, dtype=float).reshape(1, -1), distance_km
