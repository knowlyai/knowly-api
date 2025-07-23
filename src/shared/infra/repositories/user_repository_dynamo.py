import time
import uuid
from decimal import Decimal
from typing import List, Optional

from src.shared.domain.entities.subscription import Subscription
from src.shared.domain.entities.transaction import Transaction
from src.shared.domain.entities.user import User
from src.shared.domain.enums.plan_enum import PlanEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.dto.subscription_dynamo_dto import SubscriptionDynamoDTO
from src.shared.infra.dto.transaction_dynamo_dto import TransactionDynamoDTO
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO
from src.shared.infra.external.dynamo.datasources.dynamo_datasource import DynamoDatasource


class UserRepositoryDynamo(IUserRepository):

    @staticmethod
    def user_partition_key_format(user_id: str) -> str:
        return f"USER#{user_id}"

    @staticmethod
    def user_sort_key_format() -> str:
        return f"PROFILE"

    @staticmethod
    def subscription_partition_key_format(user_id: str) -> str:
        return f"USER#{user_id}"

    @staticmethod
    def subscription_sort_key_format(sub_id: str) -> str:
        return f"SUB#{sub_id}"

    @staticmethod
    def transaction_partition_key_format(user_id: str) -> str:
        return f"USER#{user_id}"

    @staticmethod
    def transaction_sort_key_format(tran_id: str) -> str:
        return f"TRAN#{tran_id}"

    def __init__(self):
        self.dynamo = DynamoDatasource(endpoint_url=Environments.get_envs().endpoint_url,
                                       dynamo_table_name=Environments.get_envs().dynamo_table_name,
                                       region=Environments.get_envs().region,
                                       partition_key=Environments.get_envs().dynamo_partition_key,
                                       sort_key=Environments.get_envs().dynamo_sort_key)
    def get_user(self, user_id: str) -> User:
        resp = self.dynamo.get_item(partition_key=self.user_partition_key_format(user_id), sort_key=self.user_sort_key_format())

        if resp.get('Item') is None:
            raise NoItemsFound("user_id")

        user_dto = UserDynamoDTO.from_dynamo(resp["Item"])
        return user_dto.to_entity()

    def create_user(self, new_user: User) -> User:
        user_dto = UserDynamoDTO.from_entity(user=new_user)
        resp = self.dynamo.put_item(partition_key=self.user_partition_key_format(new_user.user_id),
                                    sort_key=self.user_sort_key_format(), item=user_dto.to_dynamo(),
                                    is_decimal=True)
        return new_user

    def delete_user(self, user_id: str) -> User:
        resp = self.dynamo.delete_item(partition_key=self.user_partition_key_format(user_id), sort_key=self.user_sort_key_format())

        if "Attributes" not in resp:
            raise NoItemsFound("user_id")

        return UserDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def update_user(self, user_id: str, update_date: int, new_name: Optional[str], new_email: Optional[str], new_cellphone: Optional[str], new_address: Optional[str], new_cep: Optional[str]) -> User:
        self.get_user(user_id=user_id)

        item_to_update = {
            "update_date": Decimal(update_date)
        }

        if new_name is not None:
            item_to_update["name"] = new_name

        if new_email is not None:
            item_to_update["email"] = new_email

        if new_cellphone is not None:
            item_to_update["cellphone"] = new_cellphone

        if new_address is not None:
            item_to_update["address"] = new_address

        if new_cep is not None:
            item_to_update["cep"] = new_cep

        resp = self.dynamo.update_item(
            partition_key=self.user_partition_key_format(user_id),
            sort_key=self.user_sort_key_format(),
            update_dict=item_to_update
        )

        return UserDynamoDTO.from_dynamo(resp['Attributes']).to_entity()

    def get_transactions_by_user(self, user_id: str) -> List[Transaction]:
        """
        Retorna lista de transações para o usuário especificado
        """
        from boto3.dynamodb.conditions import Key

        resp = self.dynamo.query(
            key_condition_expression=Key('PK').eq(self.transaction_partition_key_format(user_id)) & Key('SK').begins_with('TRAN#')
        )

        transactions = []
        if 'Items' in resp:
            for item in resp['Items']:
                transaction_dto = TransactionDynamoDTO.from_dynamo(item)
                transactions.append(transaction_dto.to_entity())

        return transactions

    def create_transaction(self, transaction: Transaction) -> Transaction:
        transaction_dto = TransactionDynamoDTO.from_entity(transaction)

        self.dynamo.put_item(
            partition_key=self.transaction_partition_key_format(transaction.user_id),
            sort_key=self.transaction_sort_key_format(transaction.tran_id),
            item=transaction_dto.to_dynamo(),
            is_decimal=True
        )

        return transaction

    def get_subscriptions_by_user(self, user_id: str) -> List[Subscription]:
        from boto3.dynamodb.conditions import Key

        resp = self.dynamo.query(
            key_condition_expression=Key('PK').eq(self.subscription_partition_key_format(user_id)) & Key('SK').begins_with('SUB#')
        )

        subscriptions = []
        if 'Items' in resp:
            for item in resp['Items']:
                subscription_dto = SubscriptionDynamoDTO.from_dynamo(item)
                subscriptions.append(subscription_dto.to_entity())

        return subscriptions

    def create_subscription(self, subscription: Subscription) -> Subscription:
        subscription_dto = SubscriptionDynamoDTO.from_entity(subscription)

        self.dynamo.put_item(
            partition_key=self.subscription_partition_key_format(subscription.user_id),
            sort_key=self.subscription_sort_key_format(subscription.sub_id),
            item=subscription_dto.to_dynamo(),
            is_decimal=True
        )

        return subscription

    def update_subscription(self, user_id: str, new_plan: PlanEnum) -> Subscription:
        user = self.get_user(user_id)
        current_plan = user.plan

        self.dynamo.update_item(
            partition_key=self.user_partition_key_format(user_id),
            sort_key=self.user_sort_key_format(),
            update_dict={"plan": new_plan.value}
        )

        new_subscription = Subscription(
            sub_id=str(uuid.uuid4()),
            user_id=user_id,
            previous_plan=current_plan,
            new_plan=new_plan,
            update_date=int(time.time())
        )

        return self.create_subscription(new_subscription)
