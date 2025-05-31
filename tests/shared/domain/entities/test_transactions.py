from src.shared.domain.entities.transactions import Transaction
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.domain_errors import EntityError
import pytest

class Test_Transaction:
    def test_valid_transaction(self):
        transaction = Transaction(
            id="123e4567-e89b-12d3-a456-426614174000",
            user_id="user-1",
            plan=PLAN.BRONZE,
            value=99.99,
            create_date=1700000000
        )

        assert transaction.id == "123e4567-e89b-12d3-a456-426614174000"
        assert transaction.user_id == "user-1"
        assert transaction.plan == PLAN.BRONZE
        assert transaction.value == 99.99
        assert transaction.create_date == 1700000000

    def test_id_is_none(self):
        with pytest.raises(EntityError):
            Transaction(
                id=None,
                user_id="user-1",
                plan=PLAN.BRONZE,
                value=99.99,
                create_date=1700000000
            )

    def test_id_is_not_str(self):
        with pytest.raises(EntityError):
            Transaction(
                id=123,
                user_id="user-1",
                plan=PLAN.BRONZE,
                value=99.99,
                create_date=1700000000
            )

    def test_user_id_is_none(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id=None,
                plan=PLAN.BRONZE,
                value=99.99,
                create_date=1700000000
            )

    def test_user_id_is_not_str(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id=123,
                plan=PLAN.BRONZE,
                value=99.99,
                create_date=1700000000
            )

    def test_invalid_plan(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                plan='INVALID_PLAN',
                value=99.99,
                create_date=1700000000
            )

    def test_value_is_not_float(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                plan=PLAN.BRONZE,
                value="99.99",
                create_date=1700000000
            )

    def test_value_is_negative(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                plan=PLAN.BRONZE,
                value=-10.0,
                create_date=1700000000
            )

    def test_create_date_is_not_int(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                plan=PLAN.BRONZE,
                value=99.99,
                create_date="1700000000"
            )

    def test_create_date_is_negative(self):
        with pytest.raises(EntityError):
            Transaction(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                plan=PLAN.BRONZE,
                value=99.99,
                create_date=-1
            )