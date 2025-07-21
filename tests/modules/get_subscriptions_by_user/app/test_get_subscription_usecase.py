import pytest

from src.modules.get_subscriptions_by_user.app.get_subscription_usecase import GetUserSubscriptionsUseCase
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestGetUserSubscriptionsUsecase:

    def test_get_user_subscriptions_success(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        user_id = "fdddafb9-687a-4982-a025-54fb12671932"
        subscriptions = usecase(user_id)

        assert len(subscriptions) == 1
        assert subscriptions[0].user_id == user_id

    def test_get_user_subscriptions_multiple(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        user_id = "5042b518-83ca-4cbf-84fc-c992da2506e5"
        subscriptions = usecase(user_id)

        assert len(subscriptions) == 1
        assert subscriptions[0].user_id == user_id

    def test_get_user_subscriptions_empty_list(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        user_id = "a1b2c3d4-e5f6-7890-1234-567890abcdef"
        subscriptions = usecase(user_id)

        assert len(subscriptions) == 0
        assert isinstance(subscriptions, list)

    def test_get_user_subscriptions_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        with pytest.raises(NoItemsFound):
            usecase("nonexistent-user-id")

    def test_get_user_subscriptions_invalid_user_id_type(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        with pytest.raises(EntityError):
            usecase(123)

    def test_get_user_subscriptions_invalid_user_id_none(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        with pytest.raises(EntityError):
            usecase(None)

    def test_get_user_subscriptions_empty_string(self):
        repo = UserRepositoryMock()
        usecase = GetUserSubscriptionsUseCase(repo)

        with pytest.raises(NoItemsFound):
            usecase("")
