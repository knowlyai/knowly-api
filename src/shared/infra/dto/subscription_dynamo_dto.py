from decimal import Decimal

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PlanEnum


class SubscriptionDynamoDTO:
    sub_id: str
    user_id: str
    previous_plan: PlanEnum
    new_plan: PlanEnum
    update_date: int

    def __init__(
        self,
        sub_id: str,
        user_id: str,
        previous_plan: PlanEnum,
        new_plan: PlanEnum,
        update_date: int
    ):
        self.sub_id = sub_id
        self.user_id = user_id
        self.previous_plan = previous_plan
        self.new_plan = new_plan
        self.update_date = update_date

    @staticmethod
    def from_entity(subscription: Subscription) -> "SubscriptionDynamoDTO":
        """
        Parse data from Subscription entity to SubscriptionDynamoDTO
        """
        return SubscriptionDynamoDTO(
            sub_id=subscription.sub_id,
            user_id=subscription.user_id,
            previous_plan=subscription.previous_plan,
            new_plan=subscription.new_plan,
            update_date=subscription.update_date
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from SubscriptionDynamoDTO to dict suitable for DynamoDB
        """
        return {
            "entity": "subscription",
            "sub_id": self.sub_id,
            "user_id": self.user_id,
            "previous_plan": self.previous_plan.value,
            "new_plan": self.new_plan.value,
            "update_date": Decimal(self.update_date),
        }

    @staticmethod
    def from_dynamo(item: dict) -> "SubscriptionDynamoDTO":
        """
        Parse data from DynamoDB item to SubscriptionDynamoDTO
        """
        return SubscriptionDynamoDTO(
            sub_id=item["sub_id"],
            user_id=item["user_id"],
            previous_plan=PlanEnum(item["previous_plan"]),
            new_plan=PlanEnum(item["new_plan"]),
            update_date=int(item["update_date"]),
        )

    def to_entity(self) -> Subscription:
        """
        Parse data from SubscriptionDynamoDTO to Subscription entity
        """
        return Subscription(
            sub_id=self.sub_id,
            user_id=self.user_id,
            previous_plan=self.previous_plan,
            new_plan=self.new_plan,
            update_date=self.update_date
        )

    def __repr__(self):
        return (
            f"SubscriptionDynamoDTO("
            f"sub_id={self.sub_id!r}, "
            f"user_id={self.user_id!r}, "
            f"previous_plan={self.previous_plan}, "
            f"new_plan={self.new_plan}, "
            f"update_date={self.update_date}"
            f")"
        )

    def __eq__(self, other):
        if not isinstance(other, SubscriptionDynamoDTO):
            return False
        return (
            self.sub_id == other.sub_id and
            self.user_id == other.user_id and
            self.previous_plan == other.previous_plan and
            self.new_plan == other.new_plan and
            self.update_date == other.update_date
        )