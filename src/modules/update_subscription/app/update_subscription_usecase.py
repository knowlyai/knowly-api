from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class UpdateSubscriptionUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str, new_plan: PlanEnum) -> Subscription:
        if not User.validate_user_id(user_id):
            raise EntityError("user_id")

        if not isinstance(new_plan, PlanEnum):
            raise EntityError("new_plan")

        user = self.repo.get_user(user_id)

        if user.plan == new_plan:
            raise ForbiddenAction("novo plano")

        updated_subscription = self.repo.update_subscription(user_id=user_id, new_plan=new_plan)

        return updated_subscription