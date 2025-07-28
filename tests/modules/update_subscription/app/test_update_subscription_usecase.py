import pytest

from src.modules.update_subscription.app.update_subscription_usecase import UpdateSubscriptionUseCase
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestUpdateSubscriptionUsecase:
    def test_update_subscription_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        user = repo.users[0]
        original_plan = user.plan

        new_plan = PlanEnum.SI if user.plan != PlanEnum.SI else PlanEnum.GO
        updated = usecase(user_id=user.user_id, new_plan=new_plan)

        assert updated.previous_plan == original_plan
        assert updated.new_plan == new_plan

    def test_update_subscription_usecase_wrong_id_type(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=123, new_plan=PlanEnum.GO)

    def test_update_subscription_usecase_wrong_new_plan_type(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="valid-user-id", new_plan="NOT_A_PLAN")

    def test_update_subscription_usecase_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="12345678-1234-1234-1234-123456789abc", new_plan=PlanEnum.BR)

    def test_update_subscription_usecase_same_plan_forbidden(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)
        user = repo.users[0]

        with pytest.raises(ForbiddenAction):
            usecase(user_id=user.user_id, new_plan=user.plan)

    def test_update_subscription_usecase_invalid_user_id_format(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="", new_plan=PlanEnum.GO)

    def test_update_subscription_usecase_none_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id=None, new_plan=PlanEnum.GO)

    def test_update_subscription_usecase_none_new_plan(self):
        repo = UserRepositoryMock()
        usecase = UpdateSubscriptionUseCase(repo=repo)

        with pytest.raises(EntityError):
            usecase(user_id="valid-user-id", new_plan=None)
