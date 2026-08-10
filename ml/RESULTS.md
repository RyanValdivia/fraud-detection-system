# Resultados de entrenamiento

## Estado: pipeline implementado y validado, pendiente correr con dataset real

`ml/train.py` está completo:

- `build_features()` genera las 9 columnas de `app/constants.py::FEATURE_NAMES`
  (mismas que calcula `app/features.py` en serving) a partir de las columnas
  crudas del dataset Sparkov: `category_idx`, `gender_idx`, `age`,
  `distance_km` (haversine usuario↔comercio), `hour`, `is_night`, `city_pop`,
  `velocity_1h` (transacciones previas de la misma tarjeta en la última hora).
- Entrena y compara **XGBoost**, **LightGBM**, **RandomForest**.
- Selecciona el mejor por **average precision** (no accuracy — el dataset
  tiene <1% de fraude, accuracy es engañoso).
- Guarda el ganador en `ml/models/model.pkl`.

Validado con un smoke test (datos sintéticos con el mismo schema del
dataset real): el pipeline corre de punta a punta sin errores — carga,
feature engineering, split, entrenamiento de los 3 modelos, selección y
guardado del `.pkl`. Las métricas de esa corrida **no son reales**
(datos aleatorios, sin señal de fraude verdadera), solo confirman que el
código funciona.

## Pendiente

Bloqueado por falta de acceso a Kaggle (requiere login para descargar).
Para completar:

```bash
# 1. Descargar dataset (ver data/README.md) → data/fraudTrain.csv
# 2. Entrenar
cd ml
python train.py
```

Una vez corrido con el dataset real, reemplazar esta sección con:

- Tasa de fraude real del dataset
- Tabla de average precision por modelo (XGBoost / LightGBM / RandomForest)
- Classification report del modelo ganador
- Features más importantes (`model.feature_importances_` / SHAP)
