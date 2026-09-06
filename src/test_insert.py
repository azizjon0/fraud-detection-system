from database import SessionLocal
from models import Transaction


db = SessionLocal()

try:
    transaction = Transaction(
        step=1,
        transaction_type="TRANSFER",
        amount=1500.0,

        name_orig="C123456",
        old_balance_orig=5000.0,

        name_dest="C987654",
        old_balance_dest=1000.0,

        orig_balance_zero=False,
        amount_to_orig_balance=1500 / 5000,

        fraud_probability=0.82,
        predicted_fraud=True,

        actual_fraud=True
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    print("Inserted transaction ID:", transaction.id)

finally:
    db.close()