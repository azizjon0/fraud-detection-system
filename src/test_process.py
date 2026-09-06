from process_transaction import process_transaction


transaction = process_transaction(
    step=356,
    transaction_type="TRANSFER",
    amount=5000,
    name_orig="C100001",
    old_balance_orig=5000,
    name_dest="C200001",
    old_balance_dest=100,
    actual_fraud=True
)

print("Transaction ID:", transaction.id)
print("Fraud probability:", transaction.fraud_probability)
print("Predicted fraud:", transaction.predicted_fraud)