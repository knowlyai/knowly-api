import pytest

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.helpers.errors.domain_errors import EntityError, UpdateToSamePlanError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction


class TestSubscription:
    def test_valid_subscription(self):
        subscription = Subscription(
            sub_id="123e4567-e89b-12d3-a456-426614174000",
            user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.SI,
            update_date=1700000000
        )

        assert subscription.sub_id == "123e4567-e89b-12d3-a456-426614174000"
        assert subscription.user_id == "6011c94d-d574-42bf-8ec0-006efec862d1"
        assert subscription.previous_plan == PlanEnum.BR
        assert subscription.new_plan == PlanEnum.SI
        assert subscription.update_date == 1700000000

    def test_sub_id_is_none(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id=None,
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_sub_id_is_not_str(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id=123,
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_sub_id_invalid_uuid(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="invalid-uuid",
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_user_id_is_none(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id=None,
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_user_id_is_not_str(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id=123,
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_user_id_empty_string(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_user_id_whitespace_only(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="   ",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_invalid_previous_plan(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan="NOT_A_PlanEnum",
                new_plan=PlanEnum.SI,
                update_date=1700000000
            )

    def test_invalid_new_plan(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan="NOT_A_PlanEnum",
                update_date=1700000000
            )

    def test_same_plan_update(self):
        with pytest.raises(ForbiddenAction):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.BR,
                update_date=1700000000
            )

    def test_update_date_is_not_int(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date="1700000000"
            )

    def test_update_date_is_negative(self):
        with pytest.raises(EntityError):
            Subscription(
                sub_id="123e4567-e89b-12d3-a456-426614174000",
                user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
                previous_plan=PlanEnum.BR,
                new_plan=PlanEnum.SI,
                update_date=-1
            )

    def test_to_dict(self):
        subscription = Subscription(
            sub_id="123e4567-e89b-12d3-a456-426614174000",
            user_id="6011c94d-d574-42bf-8ec0-006efec862d1",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        expected_dict = {
            "sub_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "6011c94d-d574-42bf-8ec0-006efec862d1",
            "previous_plan": "Bronze",
            "new_plan": "Gold",
            "update_date": 1700000000
        }

        assert subscription.to_dict() == expected_dict

