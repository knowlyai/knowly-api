import time
from typing import List
from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.domain.repositories.subscription_repository_interface import ISubscriptionRepository
from src.shared.helpers.errors.domain_errors import EntityError, ForbiddenError

class UpdateSubscriptionUseCase:
    def __init__(self, repo: ISubscriptionRepository):
        self.repo = repo

    def __call__(self, user_id: str, new_plan: PLAN) -> Subscription:
        if not isinstance(user_id, str) or not user_id.strip():
            raise EntityError("user_id")

        if not isinstance(new_plan, PLAN):
            raise EntityError("new_plan")

        current = self.repo.get_subscription(subscription_id=user_id)
        if current is None:
            raise EntityError("subscription", "Assinatura não encontrada")

        if current.plan == new_plan:
            raise ForbiddenError("new_plan", "O novo plano deve ser diferente do plano atual")
        
        
        current.previous_plan = current.plan
        current.new_plan = new_plan
        current.update_date = int(time.time())

        updated_subscription = self.repo.update_subscription(
            subscription_id=user_id,
            new_plan=new_plan
        )

        return updated_subscription