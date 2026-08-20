"""Constantes compartidas entre entrenamiento (ml/train.py) y serving (app/features.py).

Deben mantenerse idénticas en ambos lados: si el orden/valores de CATEGORIES
cambia, hay que reentrenar el modelo.
"""

# Categorías de comercio del dataset Sparkov (kartik2112/fraud-detection).
CATEGORIES = [
    "entertainment",
    "food_dining",
    "gas_transport",
    "grocery_net",
    "grocery_pos",
    "health_fitness",
    "home",
    "kids_pets",
    "misc_net",
    "misc_pos",
    "personal_care",
    "shopping_net",
    "shopping_pos",
    "travel",
]

FEATURE_NAMES = [
    "amt",
    "category_idx",
    "gender_idx",
    "age",
    "distance_km",
    "hour",
    "is_night",
    "city_pop",
    "velocity_1h",
]
