from uuid import UUID
from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.domain.repositories.subscription_repository_interface import ISubscriptionRepository
from src.shared.helpers.errors.domain_errors import EntityError

class UpdateSubscriptionUsecase:
    def __init__(self, repo: ISubscriptionRepository):
        self.repo = repo

    def __call__(self, subscription_id: str, new_plan: PLAN) -> Subscription:
        if not Subscription.validate_id(subscription_id):
            raise EntityError("subscription_id")

        if not isinstance(new_plan, PLAN):
            raise EntityError("new_plan")

        updated_subscription = self.repo.update_subscription(
            subscription_id=subscription_id,
            new_plan=new_plan
        )
        return updated_subscription