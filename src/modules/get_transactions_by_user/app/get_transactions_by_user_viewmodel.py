from typing import List, Dict

from src.shared.domain.entities.transactions import Transaction


class TransactionViewmodel:
    """
    Converte uma única entidade Transaction em dicionário.
    """
    def __init__(self, transaction: Transaction):
        self.id = transaction.id
        self.user_id = transaction.user_id
        self.plan = transaction.plan.name
        self.value = transaction.value
        self.create_date = transaction.create_date

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan": self.plan,
            "value": self.value,
            "create_date": self.create_date
        }


class GetTransactionsByUserViewmodel:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = [TransactionViewmodel(t).to_dict() for t in transactions]

    def to_dict(self) -> Dict:
        return {
            "transactions": self.transactions,
            "message": "transactions retrieved successfully"
        }