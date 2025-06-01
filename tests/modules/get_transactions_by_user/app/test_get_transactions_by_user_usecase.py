import pytest

from src.modules.get_transactions_by_user.app.get_transactions_by_user_usecase import GetTransactionsByUserUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.transaction_repository_mock import TransactionRepositoryMock

observability = ObservabilityMock(module_name="get_transactions_by_user")


class Test_GetTransactionsByUserUsecase:

    def test_get_transactions_by_user_success(self):
        repo = TransactionRepositoryMock()
        usecase = GetTransactionsByUserUsecase(repo=repo, observability=observability)

        first_tx = repo.transactions[0]
        valid_user_id = first_tx.user_id

        result = usecase(user_id=valid_user_id)

        assert isinstance(result, list)
        assert all(tx.user_id == valid_user_id for tx in result)

    def test_get_transactions_by_user_invalid_type(self):
        repo = TransactionRepositoryMock()
        usecase = GetTransactionsByUserUsecase(repo=repo, observability=observability)

        with pytest.raises(EntityError):
            usecase(user_id=123)  