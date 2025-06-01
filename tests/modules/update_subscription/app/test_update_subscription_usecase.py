import pytest

from src.modules.update_subscription.app.update_subscription_usecase import UpdateSubscriptionUsecase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.infra.repositories.subscription_repository_mock import SubscriptionRepositoryMock
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class Test_UpdateSubscriptionUsecase:
    def test_update_subscription_usecase(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)
        existing = repo.subscriptions[0]
        updated = usecase(subscription_id=existing.id, new_plan=PLAN.SILVER)

        assert updated.previous_plan == existing.new_plan 
        assert updated.new_plan == PLAN.SILVER

    def test_update_subscription_usecase_wrong_id_type(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(subscription_id=123, new_plan=PLAN.GOLD)

    def test_update_subscription_usecase_wrong_new_plan_type(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)

        with pytest.raises(EntityError):
            usecase(subscription_id="sub-1", new_plan="NOT_A_PLAN")

    def test_update_subscription_usecase_not_found(self):
        repo = SubscriptionRepositoryMock()
        usecase = UpdateSubscriptionUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(subscription_id="nonexistent-id", new_plan=PLAN.BRONZE)