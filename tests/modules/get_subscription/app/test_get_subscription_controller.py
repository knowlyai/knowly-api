import pytest

from src.modules.get_subscription.app.get_subscription_controller import GetSubscriptionController
from src.modules.get_subscription.app.get_subscription_usecase import GetSubscriptionUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.subscription_repository_mock import SubscriptionRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound


observability = ObservabilityMock(module_name="get_subscription")


class Test_GetSubscriptionController:
    def test_get_subscription_controller(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUsecase(repo=repo, observability=observability)
        controller = GetSubscriptionController(usecase=usecase, observability=observability)

        existing = repo.subscriptions[1]
        request = HttpRequest(query_params={"id": existing.id})

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert body["id"] == existing.id
        assert body["user_id"] == existing.user_id
        assert body["previous_plan"] == existing.previous_plan.value
        assert body["new_plan"] == existing.new_plan.value
        assert body["update_date"] == existing.update_date
        assert "message" in body and isinstance(body["message"], str)

    def test_get_subscription_controller_missing_parameters(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUsecase(repo=repo, observability=observability)
        controller = GetSubscriptionController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field id is missing"

    def test_get_subscription_controller_wrong_type_parameter(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUsecase(repo=repo, observability=observability)
        controller = GetSubscriptionController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={"id": 123})

        response = controller(request=request)

        assert response.status_code == 400
        expected = (
            "Field id isn't in the right type.\n"
            " Received: int.\n"
            " Expected: str"
        )
        assert response.body == expected

    def test_get_subscription_controller_entity_error(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUsecase(repo=repo, observability=observability)
        controller = GetSubscriptionController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={"id": ""})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field id is not valid"

    def test_get_subscription_controller_no_items_found(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUsecase(repo=repo, observability=observability)
        controller = GetSubscriptionController(usecase=usecase, observability=observability)

        request = HttpRequest(query_params={"id": "nonexistent-id"})

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for subscription_id"