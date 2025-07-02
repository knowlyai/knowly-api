from typing import List

from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.repositories.transaction_repository_interface import ITransactionRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetTransactionsByUserUsecase:
    def __init__(self, repo: ITransactionRepository, observability=None):
        self.repo = repo

    def __call__(self, user_id: str) -> List[Transaction]:
        if not isinstance(user_id, str):
            raise EntityError("user_id")

        transactions = self.repo.get_all_transactions_by_user(user_id=user_id)

        return transactions
