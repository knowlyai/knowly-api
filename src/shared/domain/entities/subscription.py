import abc

from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.domain_errors import EntityError

class Subscription(abc.ABC):
    id: str
    user_id: str
    previous_plan: PLAN
    new_plan: PLAN
    update_date: int

    def __init__(
        self,
        id: str,
        user_id: str,
        previous_plan: PLAN,
        new_plan: PLAN,
        update_date: int
    ):
        if not self.validate_id(id):
            raise EntityError("id")
        self.id = id

        if not self.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not isinstance(previous_plan, PLAN):
            raise EntityError("previous_plan")
        self.previous_plan = previous_plan

        if not isinstance(new_plan, PLAN):
            raise EntityError("new_plan")
        self.new_plan = new_plan

        if not isinstance(update_date, int) or update_date < 0:
            raise EntityError("update_date")
        self.update_date = update_date

    @staticmethod
    def validate_id(id: str) -> bool:
        return isinstance(id, str) and len(id.strip()) > 0

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        return isinstance(user_id, str) and len(user_id.strip()) > 0

    def __repr__(self):
        return (
            f"SubscriptionTransaction("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"previous_plan={self.previous_plan}, "
            f"new_plan={self.new_plan}, "
            f"update_date={self.update_date}"
            f")"
        )