import pytest

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.helpers.errors.domain_errors import EntityError


class Test_Subscription:
    def test_valid_subscription(self):
        subscription = Subscription(
            id="123e4567-e89b-12d3-a456-426614174000",
            user_id="user-1",
            previous_plan=PLAN.BRONZE,
            new_plan=PLAN.SILVER,
            update_date=1700000000
        )

        assert subscription.id == "123e4567-e89b-12d3-a456-426614174000"
        assert subscription.user_id == "user-1"
        assert subscription.previous_plan == PLAN.BRONZE
        assert subscription.new_plan == PLAN.SILVER
        assert subscription.update_date == 1700000000

    def test_id_is_none(self):
        with pytest.raises(EntityError):
            Subscription(
                id=None,
                user_id="user-1",
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date=1700000000
            )

    def test_id_is_not_str(self):
        with pytest.raises(EntityError):
            Subscription(
                id=123,
                user_id="user-1",
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date=1700000000
            )

    def test_user_id_is_none(self):
        with pytest.raises(EntityError):
            Subscription(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id=None,
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date=1700000000
            )

    def test_user_id_is_not_str(self):
        with pytest.raises(EntityError):
            Subscription(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id=123,
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date=1700000000
            )

    def test_invalid_previous_plan(self):
        with pytest.raises(EntityError):
            Subscription(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                previous_plan="NOT_A_PLAN",
                new_plan=PLAN.SILVER,
                update_date=1700000000
            )

    def test_invalid_new_plan(self):
        with pytest.raises(EntityError):
            Subscription(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                previous_plan=PLAN.BRONZE,
                new_plan="NOT_A_PLAN",
                update_date=1700000000
            )

    def test_update_date_is_not_int(self):
        with pytest.raises(EntityError):
            Subscription(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date="1700000000"
            )

    def test_update_date_is_negative(self):
        with pytest.raises(EntityError):
            Subscription(
                id="123e4567-e89b-12d3-a456-426614174000",
                user_id="user-1",
                previous_plan=PLAN.BRONZE,
                new_plan=PLAN.SILVER,
                update_date=-1
            )