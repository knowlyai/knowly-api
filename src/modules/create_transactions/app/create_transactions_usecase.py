import time
from typing import Optional

from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.domain.repositories.user_repository_interface import IUserRepository


class CreateTransactionUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(
        self,
        tran_id: str,
        user_id: str,
        plan: PlanEnum,
        value: float,
        create_date: Optional[int] = None
    ):
        if hasattr(self.repo, "get_transaction") and self.repo.get_transaction(tran_id) is not None:
            raise DuplicatedItem("tran_id")

        if create_date is None:
            create_date = int(time.time())

        transaction = Transaction(
            tran_id=tran_id,
            user_id=user_id,
            plan=plan,
            value=float(value),
            create_date=create_date
        )

        return self.repo.create_transaction(transaction)