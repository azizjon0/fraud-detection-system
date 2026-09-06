from database import SessionLocal
from models import Transaction
from predict import predict_transaction


def process_transaction(
    step,
    transaction_type,
    amount,
    name_orig,
    old_balance_orig,
    name_dest,
    old_balance_dest,
    actual_fraud=None
):
    prediction = predict_transaction(
        amount=amount,
        old_balance_orig=old_balance_orig,
        old_balance_dest=old_balance_dest
    )

    db = SessionLocal()

    try:
        transaction = Transaction(
            step=step,
            transaction_type=transaction_type,
            amount=amount,

            name_orig=name_orig,
            old_balance_orig=old_balance_orig,

            name_dest=name_dest,
            old_balance_dest=old_balance_dest,

            orig_balance_zero=prediction["orig_balance_zero"],
            amount_to_orig_balance=prediction["amount_to_orig_balance"],

            fraud_probability=prediction["fraud_probability"],
            predicted_fraud=prediction["predicted_fraud"],

            actual_fraud=actual_fraud
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    finally:
        db.close()