from src.modules.get_subscriptions_by_user.app.get_subscription_controller import GetUserSubscriptionsController
from src.modules.get_subscriptions_by_user.app.get_subscription_usecase import GetUserSubscriptionsUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetUserSubscriptionsController:

    def test_get_user_subscriptions_success(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        user_id = "fdddafb9-687a-4982-a025-54fb12671932"
        request = HttpRequest(query_params={"user_id": user_id})

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert "subscriptions" in body
        assert "message" in body
        assert isinstance(body["subscriptions"], list)
        assert len(body["subscriptions"]) == 1
        assert body["subscriptions"][0]["user_id"] == user_id
        assert body["message"] == "Assinaturas do usuário encontradas com sucesso"

    def test_get_user_subscriptions_empty_list(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        # Usuário que existe mas não tem subscriptions
        user_id = "a1b2c3d4-e5f6-7890-1234-567890abcdef"
        request = HttpRequest(query_params={"user_id": user_id})

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert "subscriptions" in body
        assert "message" in body
        assert isinstance(body["subscriptions"], list)
        assert len(body["subscriptions"]) == 0
        assert body["message"] == "Assinaturas do usuário encontradas com sucesso"

    def test_get_user_subscriptions_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={})
        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id está faltando"

    def test_get_user_subscriptions_invalid_user_id_type(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": 123})
        response = controller(request=request)

        assert response.status_code == 400
        expected = "O campo user_id não está no tipo correto.\nRecebido: int.\nEsperado: str"
        assert response.body == expected

    def test_get_user_subscriptions_empty_string(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": ""})
        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id não é válido"

    def test_get_user_subscriptions_whitespace_only(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": "   "})
        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id não é válido"

    def test_get_user_subscriptions_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": "nonexistent-user-id"})
        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "Nenhum item encontrado para user_id"

    def test_get_user_subscriptions_none_value(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo=repo)
        controller = GetUserSubscriptionsController(usecase=usecase)

        request = HttpRequest(query_params={"user_id": None})
        response = controller(request=request)

        assert response.status_code == 400
        # None é tratado como parâmetro faltando, não como tipo errado
        assert response.body == "O campo user_id está faltando"
