from src.modules.create_transactions.app.create_transactions_controller import CreateTransactionController
from src.modules.create_transactions.app.create_transactions_usecase import CreateTransactionUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.enums.plan_enum import PlanEnum


class TestCreateTransactionController:

    def test_create_transaction_success_with_string_plan(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
            "value": 49.9,
            "create_date": 1724630400,
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body["message"] == "Transação criada com sucesso"
        assert response.body["transaction"]["tran_id"] == "11111111-2222-3333-4444-555555555555"
        assert response.body["transaction"]["user_id"] == repo.users[0].user_id
        assert response.body["transaction"]["plan"] == "Gold"
        assert response.body["transaction"]["value"] == 49.9
        assert response.body["transaction"]["create_date"] == 1724630400

    def test_create_transaction_success_with_enum_plan(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555556",
            "user_id": repo.users[0].user_id,
            "plan": PlanEnum.GO,
            "value": 10,
            "create_date": None,
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body["message"] == "Transação criada com sucesso"
        assert response.body["transaction"]["plan"] == "Gold"

    def test_create_transaction_missing_tran_id(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "O campo tran_id está faltando"

    def test_create_transaction_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "plan": "Gold",
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "O campo user_id está faltando"

    def test_create_transaction_missing_plan(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": repo.users[0].user_id,
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "O campo plan está faltando"

    def test_create_transaction_missing_value(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "O campo value está faltando"

    def test_create_transaction_wrong_type_tran_id(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": 123,  
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert "tran_id" in response.body

    def test_create_transaction_wrong_type_user_id(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": 999, 
            "plan": "Gold",
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert "user_id" in response.body

    def test_create_transaction_wrong_type_value(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
            "value": "10.5" 
        })

        response = controller(request)

        assert response.status_code == 400
        assert "value" in response.body

    def test_create_transaction_wrong_type_create_date(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
            "value": 10.5,
            "create_date": "1724630400", 
        })

        response = controller(request)

        assert response.status_code == 400
        assert "create_date" in response.body

    def test_create_transaction_invalid_plan_string(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": repo.users[0].user_id,
            "plan": "INVALID",  
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert "plan" in response.body

    def test_create_transaction_entity_error_blank_tran_id(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "   ",
            "user_id": repo.users[0].user_id,
            "plan": "Gold",
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 400
        assert "tran_id" in response.body

    def test_create_transaction_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)
        controller = CreateTransactionController(usecase=usecase)

        request = HttpRequest(body={
            "tran_id": "11111111-2222-3333-4444-555555555555",
            "user_id": "nonexistent-user-id",
            "plan": "Gold",
            "value": 10.0,
        })

        response = controller(request)

        assert response.status_code == 404 or response.status_code == 400
        assert "user_id" in str(response.body) or "Nenhum item encontrado" in str(response.body)