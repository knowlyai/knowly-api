import pytest

from src.modules.get_transactions_by_user.app.get_transactions_by_user_usecase import GetTransactionsByUserUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetTransactionsByUserUsecase:

    def test_get_transactions_by_user_success(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)

        first_tx = repo.transactions[0]
        valid_user_id = first_tx.user_id

        result = usecase(user_id=valid_user_id)

        assert isinstance(result, list)
        assert all(tx.user_id == valid_user_id for tx in result)

    def test_get_transactions_by_user_invalid_type(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=123)

    def test_get_transactions_by_user_no_items_found(self):
        repo = UserRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="dcd5cdaf-1c97-45fb-9319-880d244a6c66")