from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.domain_errors import EntityError
import pytest

class TestTransaction:
    def test_valid_transaction(self):
        transaction = Transaction(
            tran_id="123e4567-e89b-12d3-a456-426614174000",
            user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
            plan=PlanEnum.BR,
            value=99.99,
            create_date=1700000000
        )

        assert transaction.tran_id == "123e4567-e89b-12d3-a456-426614174000"
        assert transaction.user_id == "661ba439-6ca6-4ab8-8a55-1ee02af7dbc8"
        assert transaction.plan == PlanEnum.BR
        assert transaction.value == 99.99
        assert transaction.create_date == 1700000000

    def test_id_is_none(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id=None,
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan=PlanEnum.BR,
                value=99.99,
                create_date=1700000000
            )

    def test_id_is_not_str(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id=123,
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan=PlanEnum.BR,
                value=99.99,
                create_date=1700000000
            )

    def test_user_id_is_none(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id=None,
                plan=PlanEnum.BR,
                value=99.99,
                create_date=1700000000
            )

    def test_user_id_is_not_str(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id=123,
                plan=PlanEnum.BR,
                value=99.99,
                create_date=1700000000
            )

    def test_invalid_plan(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan='INVALID_PlanEnum',
                value=99.99,
                create_date=1700000000
            )

    def test_value_is_not_float(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan=PlanEnum.BR,
                value="99.99",
                create_date=1700000000
            )

    def test_value_is_negative(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan=PlanEnum.BR,
                value=-10.0,
                create_date=1700000000
            )

    def test_create_date_is_not_int(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan=PlanEnum.BR,
                value=99.99,
                create_date="1700000000"
            )

    def test_create_date_is_negative(self):
        with pytest.raises(EntityError):
            Transaction(
                tran_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="661ba439-6ca6-4ab8-8a55-1ee02af7dbc8",
                plan=PlanEnum.BR,
                value=99.99,
                create_date=-1
            )