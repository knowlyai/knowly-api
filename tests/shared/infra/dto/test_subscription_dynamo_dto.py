from decimal import Decimal

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.infra.dto.subscription_dynamo_dto import SubscriptionDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestSubscriptionDynamoDto:
    def test_from_entity(self):
        repo = UserRepositoryMock()
        subscription = repo.subscriptions[0]

        subscription_dto = SubscriptionDynamoDTO.from_entity(subscription=subscription)

        expected_subscription_dto = SubscriptionDynamoDTO(
            sub_id=subscription.sub_id,
            user_id=subscription.user_id,
            previous_plan=subscription.previous_plan,
            new_plan=subscription.new_plan,
            update_date=subscription.update_date
        )

        assert subscription_dto == expected_subscription_dto

    def test_to_dynamo(self):
        repo = UserRepositoryMock()
        subscription = repo.subscriptions[0]

        subscription_dto = SubscriptionDynamoDTO.from_entity(subscription=subscription)
        subscription_dynamo = subscription_dto.to_dynamo()

        expected_dict = {
            "entity": "subscription",
            "sub_id": subscription.sub_id,
            "user_id": subscription.user_id,
            "previous_plan": subscription.previous_plan.value,
            "new_plan": subscription.new_plan.value,
            "update_date": Decimal(subscription.update_date)
        }

        assert subscription_dynamo == expected_dict

    def test_from_dynamo(self):
        dynamo_dict = {
            "entity": "subscription",
            "sub_id": "fbf1af68-33c1-4f41-9290-5823158397a8",
            "user_id": "fdddafb9-687a-4982-a025-54fb12671932",
            "previous_plan": "Bronze",
            "new_plan": "Gold",
            "update_date": Decimal("1700000000")
        }

        subscription_dto = SubscriptionDynamoDTO.from_dynamo(item=dynamo_dict)

        expected_subscription_dto = SubscriptionDynamoDTO(
            sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        assert subscription_dto == expected_subscription_dto

    def test_to_entity(self):
        subscription_dto = SubscriptionDynamoDTO(
            sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        subscription = subscription_dto.to_entity()

        assert subscription.sub_id == "fbf1af68-33c1-4f41-9290-5823158397a8"
        assert subscription.user_id == "fdddafb9-687a-4982-a025-54fb12671932"
        assert subscription.previous_plan == PlanEnum.BR
        assert subscription.new_plan == PlanEnum.GO
        assert subscription.update_date == 1700000000

    def test_from_dynamo_to_entity(self):
        dynamo_item = {
            "entity": "subscription",
            "sub_id": "9cf4fdd7-f0d4-43cf-9603-e50a3033a6c3",
            "user_id": "5042b518-83ca-4cbf-84fc-c992da2506e5",
            "previous_plan": "Silver",
            "new_plan": "Bronze",
            "update_date": Decimal("1700003600")
        }

        subscription_dto = SubscriptionDynamoDTO.from_dynamo(item=dynamo_item)
        subscription = subscription_dto.to_entity()

        expected_subscription = Subscription(
            sub_id="9cf4fdd7-f0d4-43cf-9603-e50a3033a6c3",
            user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
            previous_plan=PlanEnum.SI,
            new_plan=PlanEnum.BR,
            update_date=1700003600
        )

        assert subscription.sub_id == expected_subscription.sub_id
        assert subscription.user_id == expected_subscription.user_id
        assert subscription.previous_plan == expected_subscription.previous_plan
        assert subscription.new_plan == expected_subscription.new_plan
        assert subscription.update_date == expected_subscription.update_date

    def test_from_entity_to_dynamo(self):
        repo = UserRepositoryMock()
        subscription = repo.subscriptions[1]

        subscription_dto = SubscriptionDynamoDTO.from_entity(subscription=subscription)
        subscription_dynamo = subscription_dto.to_dynamo()

        expected_dict = {
            "entity": "subscription",
            "sub_id": subscription.sub_id,
            "user_id": subscription.user_id,
            "previous_plan": subscription.previous_plan.value,
            "new_plan": subscription.new_plan.value,
            "update_date": Decimal(subscription.update_date)
        }

        assert subscription_dynamo == expected_dict

    def test_dto_equality(self):
        subscription_dto1 = SubscriptionDynamoDTO(
            sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        subscription_dto2 = SubscriptionDynamoDTO(
            sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        assert subscription_dto1 == subscription_dto2

    def test_dto_inequality(self):
        subscription_dto1 = SubscriptionDynamoDTO(
            sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        subscription_dto2 = SubscriptionDynamoDTO(
            sub_id="different-id",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        assert subscription_dto1 != subscription_dto2

    def test_repr(self):
        subscription_dto = SubscriptionDynamoDTO(
            sub_id="fbf1af68-33c1-4f41-9290-5823158397a8",
            user_id="fdddafb9-687a-4982-a025-54fb12671932",
            previous_plan=PlanEnum.BR,
            new_plan=PlanEnum.GO,
            update_date=1700000000
        )

        expected_repr = (
            "SubscriptionDynamoDTO("
            "sub_id='fbf1af68-33c1-4f41-9290-5823158397a8', "
            "user_id='fdddafb9-687a-4982-a025-54fb12671932', "
            "previous_plan=PlanEnum.BR, "
            "new_plan=PlanEnum.GO, "
            "update_date=1700000000"
            ")"
        )

        assert repr(subscription_dto) == expected_repr
