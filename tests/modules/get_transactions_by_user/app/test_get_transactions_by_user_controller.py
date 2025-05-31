import pytest

from src.modules.get_transactions_by_user.app.get_transactions_by_user_controller import GetTransactionsByUserController
from src.modules.get_transactions_by_user.app.get_transactions_by_user_usecase import GetTransactionsByUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.transaction_repository_mock import TransactionRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class Test_GetTransactionsByUserController:
    def test_get_transactions_by_user_missing_user_id(self):
        repo_trans = TransactionRepositoryMock()
        repo_user = UserRepositoryMock()
        usecase = GetTransactionsByUserUsecase(repo_trans, repo_user)
        controller = GetTransactionsByUserController(usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400

    def test_get_transactions_by_user_generic_exception_leads_to_500(self):
        class BrokenUsecase(GetTransactionsByUserUsecase):
            def __call__(self, user_id):
                raise Exception("Erro inesperado no layer de negócio")

        repo_trans = TransactionRepositoryMock()
        repo_user = UserRepositoryMock()
        usecase = BrokenUsecase(repo_trans, repo_user)
        controller = GetTransactionsByUserController(usecase)

        valid_user_id = repo_user.users[0].user_id
        request = HttpRequest(body={"user_id": valid_user_id})

        response = controller(request=request)

        assert response.status_code == 500