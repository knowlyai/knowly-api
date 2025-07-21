from typing import List

from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError


class GetTransactionsByUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str) -> List[Transaction]:
        if not isinstance(user_id, str):
            raise EntityError("user_id")

        self.repo.get_user(user_id)

        transactions = self.repo.get_transactions_by_user(user_id=user_id)

        return transactions
