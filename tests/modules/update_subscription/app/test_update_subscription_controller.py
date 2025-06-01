import pytest

from src.modules.update_subscription.app.update_subscription_controller import UpdateSubscriptionController
from src.modules.update_subscription.app.update_subscription_usecase import UpdateSubscriptionUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.subscription_repository_mock import SubscriptionRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class Test_UpdateSubscriptionController:
    def test_update_subscription_controller(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        existing = repo.subscriptions[0]
        request = HttpRequest(body={
            "id": existing.id,
            "new_plan": "GOLD"
        })

        response = controller(request=request)

        assert response.status_code == 200
        body = response.body
        assert body["id"] == existing.id
        assert body["user_id"] == existing.user_id
        assert body["previous_plan"] == "SILVER"
        assert body["new_plan"] == "GOLD"
        assert body["update_date"] == existing.update_date
        assert body["message"] == "subscription updated successfully"

    def test_update_subscription_controller_missing_id(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "new_plan": "GOLD"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field id is missing"

    def test_update_subscription_controller_missing_new_plan(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "id": "sub-1"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_plan is missing"

    def test_update_subscription_controller_invalid_id_type(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "id": 123,
            "new_plan": "GOLD"
        })

        response = controller(request=request)

        assert response.status_code == 400
        expected = (
            "Field id isn't in the right type.\n"
            " Received: int.\n"
            " Expected: str"
        )
        assert response.body == expected

    def test_update_subscription_controller_invalid_new_plan_type(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "id": "sub-1",
            "new_plan": 10
        })

        response = controller(request=request)

        assert response.status_code == 400
        expected = (
            "Field new_plan isn't in the right type.\n"
            " Received: int.\n"
            " Expected: str"
        )
        assert response.body == expected

    def test_update_subscription_controller_invalid_new_plan_value(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "id": "sub-1",
            "new_plan": "INVALID_PLAN"
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field new_plan is not valid"

    def test_update_subscription_controller_no_items_found(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo, )
        controller = UpdateSubscriptionController(usecase=usecase)

        request = HttpRequest(body={
            "id": "nonexistent-id",
            "new_plan": "GOLD"
        })

        response = controller(request=request)

        assert response.status_code == 404
        assert response.body == "No items found for subscription_id"