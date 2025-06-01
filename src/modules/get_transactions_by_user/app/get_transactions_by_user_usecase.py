from typing import List

from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.repositories.transaction_repository_interface import ITransactionRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class GetTransactionsByUserUsecase:
    def __init__(self, repo: ITransactionRepository, observability: ObservabilityAWS):
        self.repo = repo
        self.observability = observability

    def __call__(self, user_id: str) -> List[Transaction]:
        self.observability.log_usecase_in()

        if type(user_id) is not str:
            raise EntityError("user_id")

        transactions = self.repo.get_all_transactions_by_user(user_id=user_id)

        self.observability.log_usecase_out()
        return transactions