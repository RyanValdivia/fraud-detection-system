"""Utilidades geográficas y temporales compartidas.

La feature clave e innovadora de este proyecto: distancia entre la
ubicación habitual del usuario y el comercio donde ocurre la compra.
Un salto geográfico grande en poco tiempo ("viaje imposible") es una de
las señales más fuertes de fraude con tarjeta.
"""

from datetime import date, datetime

import numpy as np

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return float(EARTH_RADIUS_KM * c)


def age_from_dob(dob: date, reference: datetime) -> int:
    return (
        reference.year
        - dob.year
        - ((reference.month, reference.day) < (dob.month, dob.day))
    )
