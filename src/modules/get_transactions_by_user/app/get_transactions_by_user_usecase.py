from typing import List
from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.repositories.transaction_repository_interface import ITransactionRepository
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetTransactionsByUserUsecase:

    def __init__(self, repo_transaction: ITransactionRepository, repo_user: IUserRepository):
        self.repo_transaction = repo_transaction
        self.repo_user = repo_user

    def __call__(self, user_id: str) -> List[Transaction]:
        user = self.repo_user.get_user_by_id(user_id)

        transactions = self.repo_transaction.get_all_transactions_by_user(user_id)

        if not transactions:
            raise NoItemsFound("transactions")

        return transactions