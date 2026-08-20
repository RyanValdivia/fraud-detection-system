# Resultados de entrenamiento

## Dataset

**Sparkov Fraud Dataset** (`fraudTrain.csv`, kartik2112/fraud-detection en Kaggle)

- 1,296,675 transacciones
- 7,506 fraudes (**0.5789%** — fuertemente desbalanceado)
- split 80/20 estratificado

## Comparación de modelos

Métrica: **average precision** (AP) — la correcta acá, no accuracy (con 0.58% de fraude, un modelo que nunca predice fraude ya tiene 99.4% accuracy).

| Modelo       | Average Precision | Precision (fraude) | Recall (fraude) | F1 (fraude) |
|--------------|-------------------:|--------------------:|------------------:|-------------:|
| **LightGBM** | **0.9368**          | 0.3571               | 0.9727             | 0.5225        |
| XGBoost      | 0.9326              | 0.3458               | 0.9720             | 0.5101        |
| RandomForest | 0.8911              | 0.3097               | 0.9560             | 0.4678        |

**Ganador: LightGBM** → guardado en `ml/models/model.pkl`.

Lectura: el modelo atrapa **97.3% de los fraudes reales** (recall). El
precio es precisión baja (35.7%) — de cada 100 transacciones marcadas
"fraude", ~36 lo son de verdad y ~64 son falsos positivos. Es una
decisión de negocio esperable: en fraude casi siempre se prioriza no
dejar pasar fraude real (falso negativo caro) aunque cueste más revisión
manual (falso positivo barato). Los thresholds en `app/config.py`
(`fraud_block_threshold=0.85`, `fraud_review_threshold=0.5`) existen
justo para separar "bloquear directo" de "revisar" y así no bloquear de
más solo con el score crudo.

## Feature importance (LightGBM)

| Feature        | Importancia |
|----------------|------------:|
| `amt`          | 2485 |
| `category_idx` | 1450 |
| `age`          | 1310 |
| `hour`         | 1135 |
| `city_pop`     | 1017 |
| `distance_km`  | 751  |
| `velocity_1h`  | 332  |
| `gender_idx`   | 229  |
| `is_night`     | 90   |

`amt` y `category_idx` dominan (monto + tipo de comercio), pero
`distance_km` (la feature "viaje imposible") sí aporta señal real —
justifica el feature engineering geográfico sobre solo usar columnas
crudas del dataset.

## Reproducir

```bash
# 1. Descargar dataset (ver data/README.md) → data/fraudTrain.csv
cd ml
python train.py
```

## Pendiente / próximos pasos

- [ ] Validar contra `fraudTest.csv` (holdout separado, no visto en entrenamiento)
- [ ] Tuning de hiperparámetros (actualmente valores por defecto razonables, no optimizados)
- [ ] Ajustar `fraud_block_threshold` / `fraud_review_threshold` según curva precision-recall real, no valores arbitrarios
- [ ] SHAP para explicabilidad por transacción (`/explain` endpoint, ver conversación de uso del modelo)
