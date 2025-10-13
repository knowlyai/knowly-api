import time
import pytest

from src.modules.create_transactions.app.create_transactions_usecase import CreateTransactionUsecase
from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestCreateTransactionUsecase:

    def test_create_transaction_success(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)

        tran_id = "11111111-2222-3333-4444-555555555555"
        user_id = repo.users[0].user_id
        plan = PlanEnum.GO
        value = 49.9
        create_date = 1724630400

        result = usecase(
            tran_id=tran_id,
            user_id=user_id,
            plan=plan,
            value=value,
            create_date=create_date
        )

        assert isinstance(result, Transaction)
        assert result.tran_id == tran_id
        assert result.user_id == user_id
        assert result.plan == plan
        assert result.value == value
        assert result.create_date == create_date

    def test_create_transaction_auto_create_date_when_none(self, monkeypatch):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)

        fixed_ts = 1_700_000_000

        monkeypatch.setattr(time, "time", lambda: fixed_ts + 0.42)

        tran_id = "22222222-3333-4444-5555-666666666666"
        user_id = repo.users[0].user_id
        plan = PlanEnum.GO
        value = 10.0

        result = usecase(
            tran_id=tran_id,
            user_id=user_id,
            plan=plan,
            value=value,
            create_date=None
        )

        assert isinstance(result, Transaction)
        assert result.create_date == fixed_ts  # int(time.time())

    def test_create_transaction_casts_value_to_float(self):
        repo = UserRepositoryMock()
        usecase = CreateTransactionUsecase(repo=repo)

        tran_id = "33333333-4444-5555-6666-777777777777"
        user_id = repo.users[0].user_id
        plan = PlanEnum.GO

        result = usecase(
            tran_id=tran_id,
            user_id=user_id,
            plan=plan,
            value=50,  # int
            create_date=1724630401
        )

        assert isinstance(result, Transaction)
        assert isinstance(result.value, float)
        assert result.value == 50.0