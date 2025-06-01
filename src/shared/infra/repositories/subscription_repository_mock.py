from typing import List

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.domain.repositories.subscription_repository_interface import ISubscriptionRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class SubscriptionRepositoryMock(ISubscriptionRepository):
    subscriptions: List[Subscription]
    subscription_counter: int

    def __init__(self):
        self.subscriptions = [
            Subscription(
                id="sub-1",
                user_id="user-1",
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date=1700000000
            ),
            Subscription(
                id="sub-2",
                user_id="user-2",
                previous_plan=PLAN.SILVER,
                new_plan=PLAN.GOLD,
                update_date=1700003600
            ),
            Subscription(
                id="sub-3",
                user_id="user-3",
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.GOLD,
                update_date=1700007200
            ),
        ]
        self.subscription_counter = len(self.subscriptions)

    def get_subscription(self, subscription_id: str) -> Subscription:
        for sub in self.subscriptions:
            if sub.id == subscription_id:
                return sub
        raise NoItemsFound("subscription_id")

    def get_all_subscription(self) -> List[Subscription]:
        return self.subscriptions

    def create_subscription(self, new_subscription: Subscription) -> Subscription:
        self.subscriptions.append(new_subscription)
        self.subscription_counter += 1
        return new_subscription

    def delete_subscription(self, subscription_id: str) -> Subscription:
        for idx, sub in enumerate(self.subscriptions):
            if sub.id == subscription_id:
                return self.subscriptions.pop(idx)
        raise NoItemsFound("subscription_id")

    def update_subscription(self, subscription_id: str, new_plan: PLAN) -> Subscription:
        for sub in self.subscriptions:
            if sub.id == subscription_id:
                sub.previous_plan = sub.new_plan
                sub.new_plan = new_plan
                return sub

        raise NoItemsFound("subscription_id")

    def get_subscription_counter(self) -> int:
        return self.subscription_counter