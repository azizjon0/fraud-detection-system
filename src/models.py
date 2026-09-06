from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from src.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    step = Column(Integer, nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)

    name_orig = Column(String(100))
    old_balance_orig = Column(Float)

    name_dest = Column(String(100))
    old_balance_dest = Column(Float)

    orig_balance_zero = Column(Boolean)
    amount_to_orig_balance = Column(Float)

    fraud_probability = Column(Float)
    predicted_fraud = Column(Boolean)

    actual_fraud = Column(Boolean)

    created_at = Column(DateTime, server_default=func.now())