from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.enums.plan_enum import PLAN
from src.shared.domain.repositories.subscription_repository_interface import ISubscriptionRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.subscription_dynamo_dto import SubscriptionDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource
from src.shared.environments import Environments


class SubscriptionRepositoryDynamo(ISubscriptionRepository):

    @staticmethod
    def partition_key_format(subscription_id: str) -> str:
        return f"subscription#{subscription_id}"

    @staticmethod
    def sort_key_format(subscription_id: str) -> str:
        return f"#{subscription_id}"

    def __init__(self):
        self.dynamo = DynamoDatasource(
            endpoint_url=Environments.get_envs().endpoint_url,
            dynamo_table_name=Environments.get_envs().dynamo_table_name,
            region=Environments.get_envs().region,
            partition_key=Environments.get_envs().dynamo_partition_key,
            sort_key=Environments.get_envs().dynamo_sort_key
        )

    def get_subscription(self, subscription_id: str) -> Subscription:
        resp = self.dynamo.get_item(
            partition_key=self.partition_key_format(subscription_id),
            sort_key=self.sort_key_format(subscription_id)
        )
        if resp.get("Item") is None:
            raise NoItemsFound("subscription_id")

        subscription_dto = SubscriptionDynamoDTO.from_dynamo(resp["Item"])
        return subscription_dto.to_entity()

    def update_subscription(self, subscription_id: str, new_plan: PLAN) -> Subscription:
        # Primeiro, busca o registro atual para obter o new_plan atual como previous_plan
        existing = self.get_subscription(subscription_id)

        update_dict = {
            "previous_plan": existing.new_plan.value,
            "new_plan": new_plan.value
        }

        resp = self.dynamo.update_item(
            partition_key=self.partition_key_format(subscription_id),
            sort_key=self.sort_key_format(subscription_id),
            update_dict=update_dict
        )

        if "Attributes" not in resp:
            raise NoItemsFound("subscription_id")

        updated_dto = SubscriptionDynamoDTO.from_dynamo(resp["Attributes"])
        return updated_dto.to_entity()