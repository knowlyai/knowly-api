import uuid

from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.domain_errors import EntityError

class Transaction:
    tran_id: str
    user_id: str
    plan: PlanEnum
    value: float
    create_date: int

    def __init__(self, tran_id: str, user_id: str, plan: PlanEnum, value: float, create_date: int):
        if not self.validate_tran_id(tran_id):
            raise EntityError("tran_id")
        self.tran_id = tran_id

        if not self.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not isinstance(plan, PlanEnum):
            raise EntityError("plan")
        self.plan = plan

        if not isinstance(value, float) or value < 0:
            raise EntityError("value")
        self.value = value

        if not isinstance(create_date, int) or create_date < 0:
            raise EntityError("create_date")
        self.create_date = create_date

    @staticmethod
    def validate_tran_id(tran_id: str) -> bool:
        if tran_id is None or type(tran_id) != str:
            return False
        try:
            uuid.UUID(tran_id)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if user_id is None or type(user_id) != str:
            return False
        try:
            uuid.UUID(user_id)
            return True
        except ValueError:
            return False

    def to_dict(self) -> dict:
        return {
            "tran_id": self.tran_id,
            "user_id": self.user_id,
            "plan": self.plan.value,
            "value": self.value,
            "create_date": self.create_date,
        }
