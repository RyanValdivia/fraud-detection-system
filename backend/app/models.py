from sqlalchemy import Column, String, Float, Date, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, index=True)
    cc_num = Column(String, nullable=False)
    amt = Column(Float, nullable=False)
    merchant = Column(String, nullable=False)
    category = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    city_pop = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    merch_lat = Column(Float, nullable=False)
    merch_long = Column(Float, nullable=False)
    trans_time = Column(DateTime, nullable=False)

    fraud_probability = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())