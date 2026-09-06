from fastapi import FastAPI, Query
from pydantic import BaseModel

from src.database import Base, engine, SessionLocal
from src.models import Transaction
from src.process_transaction import process_transaction


app = FastAPI(
    title="Fraud Detection API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


class TransactionRequest(BaseModel):
    step: int
    transaction_type: str
    amount: float
    name_orig: str
    old_balance_orig: float
    name_dest: str
    old_balance_dest: float


class PredictionResponse(BaseModel):
    transaction_id: int
    fraud_probability: float
    predicted_fraud: bool


@app.get("/")
def root():
    return {
        "message": "Fraud Detection API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: TransactionRequest):
    result = process_transaction(
        step=transaction.step,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount,
        name_orig=transaction.name_orig,
        old_balance_orig=transaction.old_balance_orig,
        name_dest=transaction.name_dest,
        old_balance_dest=transaction.old_balance_dest
    )

    return PredictionResponse(
        transaction_id=result.id,
        fraud_probability=result.fraud_probability,
        predicted_fraud=result.predicted_fraud
    )


@app.get("/stats")
def get_stats():
    db = SessionLocal()

    try:
        total = db.query(Transaction).count()

        fraud = (
            db.query(Transaction)
            .filter(Transaction.predicted_fraud.is_(True))
            .count()
        )

        fraud_rate = fraud / total if total else 0

        return {
            "total_transactions": total,
            "fraud_transactions": fraud,
            "fraud_rate": fraud_rate
        }

    finally:
        db.close()


@app.get("/transactions")
def get_transactions(
    limit: int = Query(default=20, ge=1, le=100)
):
    db = SessionLocal()

    try:
        transactions = (
            db.query(Transaction)
            .order_by(Transaction.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": tx.id,
                "step": tx.step,
                "transaction_type": tx.transaction_type,
                "amount": tx.amount,
                "name_orig": tx.name_orig,
                "old_balance_orig": tx.old_balance_orig,
                "name_dest": tx.name_dest,
                "old_balance_dest": tx.old_balance_dest,
                "orig_balance_zero": tx.orig_balance_zero,
                "amount_to_orig_balance": tx.amount_to_orig_balance,
                "fraud_probability": tx.fraud_probability,
                "predicted_fraud": tx.predicted_fraud,
                "actual_fraud": tx.actual_fraud,
                "created_at": tx.created_at
            }
            for tx in transactions
        ]

    finally:
        db.close()