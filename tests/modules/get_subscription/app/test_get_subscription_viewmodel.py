import pytest

from src.modules.get_subscription.app.get_subscription_viewmodel import GetSubscriptionViewmodel
from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN


class Test_GetSubscriptionViewmodel:
    def test_get_subscription_viewmodel(self):
        subscription = Subscription(
            id="sub-123",
            user_id="user-42",
            previous_plan=PLAN.BRONZE,
            new_plan=PLAN.SILVER,
            update_date=1700000000
        )
        viewmodel_dict = GetSubscriptionViewmodel(subscription).to_dict()

        expected = {
            "id": "sub-123",
            "user_id": "user-42",
            "previous_plan": "BRONZE",
            "new_plan": "SILVER",
            "update_date": 1700000000,
            "message": "subscription retrieved successfully"
        }

        assert viewmodel_dict == expected