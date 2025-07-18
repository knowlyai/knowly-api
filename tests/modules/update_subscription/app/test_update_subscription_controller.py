from src.modules.update_subscription.app.update_subscription_controller import UpdateSubscriptionController
from src.modules.update_subscription.app.update_subscription_usecase import UpdateSubscriptionUseCase
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUpdateSubscriptionController:
    def test_update_subscription_controller(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        existing_user = repo.users[0]
        original_plan = existing_user.plan.value
        new_plan_str = "SI" if existing_user.plan.value != "Silver" else "GO"

        request = HttpRequest(body={
            "user_id": existing_user.user_id,
            "new_plan": new_plan_str
        })

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert body["subscription"]["user_id"] == existing_user.user_id
        assert body["subscription"]["previous_plan"] == original_plan
        expected_new_plan = PlanEnum[new_plan_str].value
        assert body["subscription"]["new_plan"] == expected_new_plan
        assert "sub_id" in body["subscription"]
        assert "update_date" in body["subscription"]
        assert body["message"] == "subscription updated successfully"

    def test_update_subscription_controller_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "new_plan": "GO"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id está faltando"

    def test_update_subscription_controller_missing_new_plan(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "fdddafb9-687a-4982-a025-54fb12671932"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo new_plan está faltando"

    def test_update_subscription_controller_invalid_user_id_type(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": 123,
            "new_plan": "GO"
        })

        response = controller(request=request)

        assert response.status_code == 400
        expected = (
            "O campo user_id não está no tipo correto.\n"
            "Recebido: int.\n"
            "Esperado: str"
        )
        assert response.body == expected

    def test_update_subscription_controller_invalid_new_plan_type(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
            "new_plan": 10
        })

        response = controller(request=request)

        assert response.status_code == 400
        expected = (
            "O campo new_plan não está no tipo correto.\n"
            "Recebido: int.\n"
            "Esperado: str"
        )
        assert response.body == expected

    def test_update_subscription_controller_invalid_new_plan_value(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
            "new_plan": "INVALID_PLAN"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo new_plan não é válido"

    def test_update_subscription_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "12345678-1234-1234-1234-123456789abc",
            "new_plan": "GO"
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "Nenhum item encontrado para user_id"

    def test_update_subscription_controller_same_plan_forbidden(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        existing_user = repo.users[0]
        current_plan_str = existing_user.plan.name  # Usa o nome do enum (GO, SI, BR)

        request = HttpRequest(body={
            "user_id": existing_user.user_id,
            "new_plan": current_plan_str
        })

        response = controller(request=request)

        assert response.status_code == 403
        assert response.body == "Essa ação é proibida para novo plano"

    def test_update_subscription_controller_invalid_user_id_format(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "",
            "new_plan": "GO"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "O campo user_id não é válido"
