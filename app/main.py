from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import Base, engine, get_db
from app.features import build_feature_vector
from app.model import fraud_model
from app.schemas import FraudPrediction, TransactionRequest

app = FastAPI(
    title="Fraud Detection System",
    description="API de scoring de fraude en tiempo real usando ML clásico (XGBoost/LightGBM/RandomForest).",
    version="0.1.0",
)


Base.metadata.create_all(bind=engine)


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key",
        )

    return x_api_key


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": fraud_model.model is not None,
    }


@app.post("/predict", response_model=FraudPrediction)
def predict(
    transaction: TransactionRequest,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    # 1. Generar features
    features, distance_km = build_feature_vector(transaction)

    # 2. Ejecutar modelo
    probability = fraud_model.predict_proba(features)
    decision = fraud_model.decide(probability)

    # 3. Crear registro para PostgreSQL
    db_transaction = models.Transaction(
        transaction_id=transaction.transaction_id,
        cc_num=transaction.cc_num,
        amt=transaction.amt,
        merchant=transaction.merchant,
        category=transaction.category,
        gender=transaction.gender,
        dob=transaction.dob,
        city_pop=transaction.city_pop,
        lat=transaction.lat,
        long=transaction.long,
        merch_lat=transaction.merch_lat,
        merch_long=transaction.merch_long,
        trans_time=transaction.trans_time,
        fraud_probability=round(probability, 4),
        decision=decision,
        distance_km=round(distance_km, 2),
    )

    # 4. Guardar en PostgreSQL
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    # 5. Responder al cliente
    return FraudPrediction(
        transaction_id=transaction.transaction_id,
        fraud_probability=round(probability, 4),
        decision=decision,
        distance_km=round(distance_km, 2),
    )


@app.get("/transactions/{transaction_id}")
def get_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.transaction_id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    return transaction
