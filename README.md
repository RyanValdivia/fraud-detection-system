# Fraud Detection System

API que analiza transacciones en tiempo real y devuelve una probabilidad de fraude usando modelos de Machine Learning clásico (no requiere GPU ni LLM).

```
Compra → Feature Engineering → Modelo ML → Probabilidad de fraude → Decisión (permitir / revisar / bloquear)
```

## Dataset

**Sparkov Fraud Dataset** ([kartik2112/fraud-detection](https://www.kaggle.com/datasets/kartik2112/fraud-detection), Kaggle): ~1.3M transacciones simuladas con datos ricos por transacción (comercio, categoría, geolocalización de usuario y comercio, demografía del titular). Ver `data/README.md` para instrucciones de descarga.

**Feature diferenciador**: distancia geográfica (haversine) entre la ubicación habitual del usuario y el comercio donde ocurre la compra en el momento de la transacción — señal clásica de "viaje imposible" usada en detección de fraude real, combinada con velocidad de transacciones (Redis) y patrones por categoría/hora/edad.

## Stack

- **API**: FastAPI
- **Base de datos**: PostgreSQL
- **Cache / feature store rápido**: Redis (contador de velocidad de transacciones por tarjeta)
- **Contenedores**: Docker / Docker Compose
- **Modelos ML**: XGBoost, LightGBM, Random Forest — se entrenan los tres y se guarda el de mejor *average precision* (métrica correcta dado el fuerte desbalance fraude/no-fraude)

## Estructura

```
.
├── app/
│   ├── main.py          # Endpoints FastAPI
│   ├── config.py        # Configuración (env vars)
│   ├── database.py      # Conexión PostgreSQL
│   ├── cache.py         # Conexión Redis
│   ├── schemas.py       # Modelos Pydantic (request/response)
│   ├── features.py      # Feature engineering
│   └── model.py         # Carga y predicción del modelo
├── ml/
│   ├── train.py         # Entrenamiento del modelo
│   └── models/          # Modelos serializados (.pkl / .joblib)
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Cómo funciona

1. Llega una transacción vía `POST /predict`.
2. Se generan features (monto, hora, frecuencia, ubicación, historial, etc.).
3. El modelo entrenado (XGBoost/LightGBM/RandomForest) calcula `probabilidad de fraude`.
4. Según umbral configurable:
   - `< 0.5` → permitir
   - `0.5 - 0.85` → revisar manualmente
   - `> 0.85` → bloquear

## Levantar el proyecto

```bash
cp .env.example .env
docker compose up --build
```

API disponible en `http://localhost:8000/docs`.

## Entrenar el modelo

```bash
# 1. Descargar dataset (ver data/README.md)
# 2. Entrenar (compara XGBoost / LightGBM / RandomForest, guarda el mejor)
python ml/train.py
```

Genera el artefacto en `ml/models/model.pkl`, que la API carga al iniciar.

## Ejemplo de request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "tx_001",
    "cc_num": "4111111111111111",
    "amt": 120.50,
    "merchant": "fraud_Kirlin and Sons",
    "category": "shopping_pos",
    "gender": "F",
    "dob": "1990-05-14",
    "city_pop": 50000,
    "lat": -12.0464,
    "long": -77.0428,
    "merch_lat": -12.10,
    "merch_long": -77.05,
    "trans_time": "2026-08-05T14:30:00"
  }'
```

## Endpoints principales

| Método | Ruta        | Descripción                              |
|--------|-------------|-------------------------------------------|
| GET    | `/health`   | Estado del servicio                       |
| POST   | `/predict`  | Recibe una transacción, devuelve score    |
| GET    | `/transactions/{id}` | Consulta histórico de una transacción |

## Qué se aprende con este proyecto

- ML clásico para datos tabulares (sigue siendo muy competitivo vs LLMs para este tipo de problema)
- Diseño de APIs de inferencia (model serving)
- Feature engineering para detección de fraude
- Arquitectura de servicios (API + DB + Cache + contenedores)

## Roadmap

- [ ] Endpoint de reentrenamiento
- [ ] Monitoreo de drift del modelo
- [ ] Autenticación de API (API Key / JWT)
- [ ] Persistir cada predicción en PostgreSQL (tabla `transactions`)
