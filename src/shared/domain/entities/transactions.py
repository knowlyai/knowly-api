import abc

from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.domain_errors import EntityError

class Transaction(abc.ABC):
    id: str
    user_id: str
    plan: PLAN
    value: float
    create_date: int

    def __init__(self, id: str, user_id: str, plan: PLAN, value: float, create_date: int):
        if not self.validate_id(id):
            raise EntityError("id")
        self.id = id

        if not self.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not isinstance(plan, PLAN):
            raise EntityError("plan")
        self.plan = plan

        if not isinstance(value, float) or value < 0:
            raise EntityError("value")
        self.value = value

        if not isinstance(create_date, int) or create_date < 0:
            raise EntityError("create_date")
        self.create_date = create_date

    @staticmethod
    def validate_id(id: str) -> bool:
        return isinstance(id, str) and len(id.strip()) > 0

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        return isinstance(user_id, str) and len(user_id.strip()) > 0

    def __repr__(self):
        return f"Transaction(id={self.id}, user_id={self.user_id}, plan={self.plan}, value={self.value}, create_date={self.create_date})"