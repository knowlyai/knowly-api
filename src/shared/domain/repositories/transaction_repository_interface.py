from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.transactions import Transaction


class ITransactionRepository(ABC):

    @abstractmethod
    def get_all_transactions_by_user(self, user_id: str) -> List[Transaction]:
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: str) -> Transaction:
        pass