# Fraud Detection System

API que analiza transacciones en tiempo real y devuelve una probabilidad de fraude usando modelos de Machine Learning clásico (no requiere GPU ni LLM).

```
Compra → Feature Engineering → Modelo ML → Probabilidad de fraude → Decisión (permitir / revisar / bloquear)
```

## Stack

- **API**: FastAPI
- **Base de datos**: PostgreSQL
- **Cache / feature store rápido**: Redis
- **Contenedores**: Docker / Docker Compose
- **Modelos ML**: XGBoost, LightGBM, Random Forest (scikit-learn)

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
python ml/train.py
```

Genera el artefacto en `ml/models/model.pkl`, que la API carga al iniciar.

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

- [ ] Entrenamiento con dataset público (ej. Kaggle Credit Card Fraud)
- [ ] Endpoint de reentrenamiento
- [ ] Monitoreo de drift del modelo
- [ ] Autenticación de API (API Key / JWT)
