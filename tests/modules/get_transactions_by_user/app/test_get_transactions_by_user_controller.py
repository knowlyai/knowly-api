import pytest

from src.modules.get_transactions_by_user.app.get_transactions_by_user_controller import (
    GetTransactionsByUserController
)
from src.modules.get_transactions_by_user.app.get_transactions_by_user_usecase import (
    GetTransactionsByUserUseCase
)
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.transaction_repository_mock import TransactionRepositoryMock


class Test_GetTransactionsByUserController:

    def test_get_transactions_by_user_success(self):
        repo = TransactionRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        first_tx = repo.transactions[0]
        request = HttpRequest(query_params={"user_id": first_tx.user_id})

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert isinstance(body, list)
        assert any(tx["user_id"] == first_tx.user_id for tx in body)
        sample = body[0]
        assert "id" in sample
        assert "plan" in sample
        assert "value" in sample
        assert "create_date" in sample

    def test_get_transactions_by_user_missing_user_id(self):
        repo = TransactionRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(query_params={})
        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id is missing"

    def test_get_transactions_by_user_invalid_user_id_type(self):
        repo = TransactionRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": 123})
        response = controller(request=request)

        assert response.status_code == 400
        expected = (
            "Field user_id isn't in the right type.\n"
            " Received: int.\n"
            " Expected: str"
        )
        assert response.body == expected

    def test_get_transactions_by_user_entity_error_empty(self):
        repo = TransactionRepositoryMock()
        usecase = GetTransactionsByUserUseCase(repo=repo)
        controller = GetTransactionsByUserController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": ""})
        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field user_id is not valid"
