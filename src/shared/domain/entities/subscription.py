import uuid

from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class Subscription:
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
        if not self.validate_sub_id(sub_id):
            raise EntityError("sub_id")
        self.sub_id = sub_id

        if not self.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not isinstance(previous_plan, PlanEnum):
            raise EntityError("previous_plan")
        self.previous_plan = previous_plan

        if not isinstance(new_plan, PlanEnum):
            raise EntityError("new_plan")
        if new_plan.value == previous_plan.value:
            raise ForbiddenAction(new_plan.value)
        self.new_plan = new_plan

        if not isinstance(update_date, int) or update_date < 0:
            raise EntityError("update_date")
        self.update_date = update_date

    @staticmethod
    def validate_sub_id(sub_id: str) -> bool:
        if sub_id is None or type(sub_id) != str:
            return False
        try:
            uuid.UUID(sub_id)
            return True
        except ValueError:
            return False


    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        return isinstance(user_id, str) and len(user_id.strip()) > 0

    def to_dict(self) -> dict:
        return {
            "sub_id": self.sub_id,
            "user_id": self.user_id,
            "previous_plan": self.previous_plan.value,
            "new_plan": self.new_plan.value,
            "update_date": self.update_date
        }