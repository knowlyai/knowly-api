from abc import ABC, abstractmethod

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN


class ISubscriptionRepository(ABC):

    @abstractmethod
    def get_subscription(self, subscription_id: str) -> Subscription:
        pass

    @abstractmethod
    def update_subscription(self, subscription_id: str, new_plan: PLAN) -> Subscription:
        pass