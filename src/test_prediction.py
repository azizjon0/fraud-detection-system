from predict import predict_transaction

result = predict_transaction(
    amount=5000,
    old_balance_orig=5000,
    old_balance_dest=100
)

print(result)