import pytest

from src.modules.get_subscription.app.get_subscription_usecase import GetSubscriptionUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.external.observability.observability_mock import ObservabilityMock
from src.shared.infra.repositories.subscription_repository_mock import SubscriptionRepositoryMock

observability = ObservabilityMock(module_name="get_subscription")


class Test_GetSubscriptionUsecase:

    def test_get_subscription(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUseCase(repo, observability=observability)

        existing = repo.subscriptions[1]
        subscription = usecase(subscription_id=existing.id)

        assert subscription == existing

    def test_get_subscription_not_found(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUseCase(repo, observability=observability)

        with pytest.raises(NoItemsFound):
            usecase(subscription_id="nonexistent-id")

    def test_get_subscription_invalid_id(self):
        repo = SubscriptionRepositoryMock()
        usecase = GetSubscriptionUseCase(repo, observability=observability)

        with pytest.raises(EntityError):
            usecase(subscription_id=123)