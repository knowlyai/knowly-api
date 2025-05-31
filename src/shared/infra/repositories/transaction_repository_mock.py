from typing import List, Optional
from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.domain.repositories.transaction_repository_interface import ITransactionRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class TransactionRepositoryMock(ITransactionRepository):
    transactions: List[Transaction]

    def __init__(self):
        self.transactions = [
            Transaction(
                id="tx-1",
                user_id="user-1",
                plan=PLAN.BRONZE,
                value=29.9,
                create_date=1717000000
            ),
            Transaction(
                id="tx-2",
                user_id="user-1",
                plan=PLAN.SILVER,
                value=59.9,
                create_date=1717100000
            ),
            Transaction(
                id="tx-3",
                user_id="user-2",
                plan=PLAN.GOLD,
                value=19.9,
                create_date=1717200000
            ),
        ]

    def get_all_transactions_by_user(self, user_id: str) -> List[Transaction]:
        return [tx for tx in self.transactions if tx.user_id == user_id]
    
    def get_transaction_by_id(self, transaction_id: str) -> Optional[Transaction]:
        return None