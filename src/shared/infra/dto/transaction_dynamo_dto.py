from decimal import Decimal

from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.enums.plan_enum import PlanEnum


class TransactionDynamoDTO:
    tran_id: str
    user_id: str
    plan: PlanEnum
    value: float
    create_date: int

    def __init__(
        self,
        tran_id: str,
        user_id: str,
        plan: PlanEnum,
        value: float,
        create_date: int
    ):
        self.tran_id = tran_id
        self.user_id = user_id
        self.plan = plan
        self.value = value
        self.create_date = create_date

    @staticmethod
    def from_entity(transaction: Transaction) -> "TransactionDynamoDTO":
        """
        Parse data from Transaction entity to TransactionDynamoDTO
        """
        return TransactionDynamoDTO(
            tran_id=transaction.tran_id,
            user_id=transaction.user_id,
            plan=transaction.plan,
            value=transaction.value,
            create_date=transaction.create_date
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from TransactionDynamoDTO to dict suitable for DynamoDB
        """
        return {
            "entity": "transaction",
            "tran_id": self.tran_id,
            "user_id": self.user_id,
            "plan": self.plan.value,
            "value": Decimal(str(self.value)),
            "create_date": Decimal(self.create_date),
        }

    @staticmethod
    def from_dynamo(item: dict) -> "TransactionDynamoDTO":
        """
        Parse data from DynamoDB item to TransactionDynamoDTO
        """
        return TransactionDynamoDTO(
            tran_id=item["tran_id"],
            user_id=item["user_id"],
            plan=PlanEnum(item["plan"]),
            value=float(item["value"]),
            create_date=int(item["create_date"]),
        )

    def to_entity(self) -> Transaction:
        """
        Parse data from TransactionDynamoDTO to Transaction entity
        """
        return Transaction(
            tran_id=self.tran_id,
            user_id=self.user_id,
            plan=self.plan,
            value=self.value,
            create_date=self.create_date
        )

    def __repr__(self):
        return (
            f"TransactionDynamoDTO("
            f"tran_id={self.tran_id!r}, "
            f"user_id={self.user_id!r}, "
            f"plan={self.plan}, "
            f"value={self.value}, "
            f"create_date={self.create_date}"
            f")"
        )

    def __eq__(self, other):
        if not isinstance(other, TransactionDynamoDTO):
            return False
        return (
            self.tran_id == other.tran_id and
            self.user_id == other.user_id and
            self.plan == other.plan and
            self.value == other.value and
            self.create_date == other.create_date
        )
