from datetime import date, datetime

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    transaction_id: str
    cc_num: str                      # identificador de tarjeta/usuario
    amt: float = Field(gt=0)
    merchant: str
    category: str                    # ver app/constants.py -> CATEGORIES
    gender: str                      # "M" | "F"
    dob: date                        # fecha de nacimiento del titular
    city_pop: int = Field(ge=0)

    # ubicación habitual del usuario (home location)
    lat: float
    long: float

    # ubicación del comercio donde ocurre la transacción
    merch_lat: float
    merch_long: float

    trans_time: datetime = Field(default_factory=datetime.utcnow)


class FraudPrediction(BaseModel):
    transaction_id: str
    fraud_probability: float
    decision: str  # "allow" | "review" | "block"
    distance_km: float
