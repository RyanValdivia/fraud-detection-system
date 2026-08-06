from datetime import datetime

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    transaction_id: str
    user_id: str
    amount: float = Field(gt=0)
    merchant_category: str
    country: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device_id: str | None = None


class FraudPrediction(BaseModel):
    transaction_id: str
    fraud_probability: float
    decision: str  # "allow" | "review" | "block"
