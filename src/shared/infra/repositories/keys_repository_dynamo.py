from typing import List

from src.shared.domain.entities.kb_key import KbKey
from src.shared.domain.repositories.keys_repository_interface import IKeysRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.kb_key_dynamo_dto import KbKeyDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class KeysRepositoryDynamo(IKeysRepository):

    @staticmethod
    def key_partition_key_format(kb_key: str) -> str:
        return f"KEY#{kb_key}"

    @staticmethod
    def gsi1_partition_key_format(user_id: str) -> str:
        return f"USER#{user_id}"

    @staticmethod
    def gsi1_sort_key_format(kb_id: str = None) -> str:
        if kb_id:
            return f"KB#{kb_id}#"
        return "KB#"

    def __init__(self):
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            endpoint_url=envs.endpoint_url,
            dynamo_table_name=envs.dynamo_keys_table_name,
            region=envs.region,
            partition_key=envs.dynamo_keys_partition_key,
            sort_key=None
        )
        self.gsi1_name = envs.dynamo_keys_gsi1_name

    def create_kb_key(self, kb_key: KbKey) -> KbKey:
        kb_key_dto = KbKeyDynamoDTO.from_entity(kb_key)

        item = kb_key_dto.to_dynamo()
        item["GSI1PK"] = self.gsi1_partition_key_format(kb_key.user_id)
        item["GSI1SK"] = f"KB#{kb_key.kb_id}#{kb_key.kb_key}"

        self.dynamo.put_item(
            partition_key=self.key_partition_key_format(kb_key.kb_key),
            item=item,
            is_decimal=False
        )

        return kb_key

    def get_kb_keys(self, user_id: str, kb_id: str = None) -> List[KbKey]:
        from boto3.dynamodb.conditions import Key

        if kb_id:
            key_condition = Key('GSI1PK').eq(self.gsi1_partition_key_format(user_id)) & \
                           Key('GSI1SK').begins_with(self.gsi1_sort_key_format(kb_id))
        else:
            key_condition = Key('GSI1PK').eq(self.gsi1_partition_key_format(user_id)) & \
                           Key('GSI1SK').begins_with(self.gsi1_sort_key_format())

        resp = self.dynamo.query(
            key_condition_expression=key_condition,
            index_name=self.gsi1_name
        )

        kb_keys: List[KbKey] = []
        for item in resp.get('Items', []):
            kb_key_dto = KbKeyDynamoDTO.from_dynamo(item)
            kb_keys.append(kb_key_dto.to_entity())

        return kb_keys

    def delete_kb_key(self, user_id: str, kb_key: str) -> KbKey:
        resp = self.dynamo.get_item(
            partition_key=self.key_partition_key_format(kb_key)
        )

        item = resp.get('Item')
        if item is None:
            raise NoItemsFound("kb_key")

        kb_key_dto = KbKeyDynamoDTO.from_dynamo(item)
        if kb_key_dto.user_id != user_id:
            raise NoItemsFound("kb_key")

        delete_resp = self.dynamo.delete_item(
            partition_key=self.key_partition_key_format(kb_key)
        )

        if "Attributes" not in delete_resp:
            raise NoItemsFound("kb_key")

        return KbKeyDynamoDTO.from_dynamo(delete_resp['Attributes']).to_entity()
