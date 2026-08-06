from fastapi import FastAPI

from app.features import build_feature_vector
from app.model import fraud_model
from app.schemas import FraudPrediction, TransactionRequest

app = FastAPI(
    title="Fraud Detection System",
    description="API de scoring de fraude en tiempo real usando ML clásico (XGBoost/LightGBM/RandomForest).",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": fraud_model.model is not None}


@app.post("/predict", response_model=FraudPrediction)
def predict(transaction: TransactionRequest):
    features = build_feature_vector(transaction)
    probability = fraud_model.predict_proba(features)
    decision = fraud_model.decide(probability)

    return FraudPrediction(
        transaction_id=transaction.transaction_id,
        fraud_probability=round(probability, 4),
        decision=decision,
    )
