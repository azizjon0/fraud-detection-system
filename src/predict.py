import os
import joblib
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")

model = joblib.load(MODEL_PATH)


def predict_transaction(
    amount,
    old_balance_orig,
    old_balance_dest
):
    orig_balance_zero = old_balance_orig == 0

    if old_balance_orig > 0:
        amount_to_orig_balance = amount / old_balance_orig
    else:
        amount_to_orig_balance = 0

    features = pd.DataFrame([{
        "amount": amount,
        "oldBalanceOrig": old_balance_orig,
        "oldBalanceDest": old_balance_dest,
        "orig_balance_zero": orig_balance_zero,
        "amount_to_orig_balance": amount_to_orig_balance
    }])

    fraud_probability = model.predict_proba(features)[0][1]
    predicted_fraud = fraud_probability >= 0.5

    return {
        "fraud_probability": float(fraud_probability),
        "predicted_fraud": bool(predicted_fraud),
        "orig_balance_zero": bool(orig_balance_zero),
        "amount_to_orig_balance": float(amount_to_orig_balance)
    }