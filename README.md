# Fraud Detection System

Monorepo: API que analiza transacciones en tiempo real y devuelve una probabilidad de fraude usando modelos de Machine Learning clásico (no requiere GPU ni LLM), más un frontend en Next.js para consumirla.

```
Compra → Feature Engineering → Modelo ML → Probabilidad de fraude → Decisión (permitir / revisar / bloquear)
```

## Estructura

```
.
├── backend/              # API FastAPI + ML + Postgres + Redis
│   ├── app/
│   ├── ml/
│   ├── tests/
│   ├── data/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/              # Next.js (App Router, TS, Tailwind)
│   ├── src/
│   ├── Dockerfile
│   └── .env.local.example
└── docker-compose.yml     # orquesta api + db + redis + frontend
```

Detalle de la API (dataset, features, endpoints, entrenamiento del modelo) en [`backend/README.md`](backend/README.md).

## Levantar todo el proyecto

```bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local   # opcional, mismo default
docker compose up --build
```

- API: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

## Levantar solo backend o solo frontend

```bash
docker compose up --build api db redis
docker compose up --build frontend
```

## Stack

- **API**: FastAPI + SQLAlchemy + PostgreSQL + Redis
- **ML**: XGBoost / LightGBM / RandomForest (ver `backend/ml/train.py`)
- **Frontend**: Next.js 16 (App Router) + TypeScript + Tailwind + shadcn/ui
- **Contenedores**: Docker / Docker Compose

## Frontend

Dos vistas en `http://localhost:3000` (tabs):

- **Evaluar**: formulario de transacción → `POST /predict` → muestra probabilidad, decisión (allow/review/block) y distancia titular-comercio.
- **Buscar**: consulta una transacción ya guardada por `transaction_id` → `GET /transactions/{id}`.

El API key nunca llega al navegador: el frontend expone rutas propias (`/api/predict`, `/api/transactions/[id]`) que corren en el servidor de Next.js y reenvían la petición al backend con `x-api-key` inyectada desde variables de entorno (`API_URL`, `API_KEY`, ver `frontend/.env.local.example`).
