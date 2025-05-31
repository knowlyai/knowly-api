from typing import List
from src.shared.domain.entities.transactions import Transaction


class TransactionViewmodel:
    transaction: Transaction

    def __init__(self, transaction: Transaction):
        self.transaction = transaction

    def to_dict(self) -> dict:
        return {
            "id": self.transaction.id,
            "user_id": self.transaction.user_id,
            "plan": self.transaction.plan.value,
            "value": self.transaction.value,
            "create_date": self.transaction.create_date
        }


class GetTransactionsByUserViewmodel:
    transactions: List[Transaction]

    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions

    def to_dict(self) -> dict:
        return {
            "transactions": [TransactionViewmodel(t).to_dict() for t in self.transactions] if self.transactions else [],
            "last_transaction_id": self.transactions[-1].id if self.transactions else None,
            "message": "the transactions were retrieved successfully"
        }