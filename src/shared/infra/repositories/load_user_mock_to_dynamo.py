from decimal import Decimal

import boto3
import dotenv

from src.shared.environments import Environments
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


def setup_dynamo_table():
    dynamo_table_name = "knowly-api-table"
    endpoint_url = "http://localhost:8000"
    print("Setting up DynamoDB table...")

    dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint_url, region_name='us-east-1')
    print("DynamoDB client created")
    tables = dynamo_client.list_tables()['TableNames']

    if dynamo_table_name not in tables:
        print("Creating table...")
        dynamo_client.create_table(
            TableName=dynamo_table_name,
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'SK',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'SK',
                    'AttributeType': 'S'
                }

            ],
            BillingMode='PAY_PER_REQUEST',
        )
        print("Waiting for table to be created...")
        dynamo_client.get_waiter('table_exists').wait(TableName=dynamo_table_name)

        print('Loading table...')

        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url, region_name='us-east-1')

        table = dynamodb.Table(dynamo_table_name)

        print("Adding counter to table")

        table.put_item(
            Item={
                'PK': 'COUNTER',
                'SK': 'COUNTER',
                'COUNTER': Decimal(0)
            }
        )

        print('Table "user_mss_template-table" created!')

    else:
        print("Table already exists!")


def load_mock_to_local_dynamo():
    setup_dynamo_table()
    mock_repo = UserRepositoryMock()
    dynamo_repo = UserRepositoryDynamo()

    count = 0

    print('Loading mock data to dynamo...')
    for user in mock_repo.users:
        print(f"Loading user {user.user_id} | {user.name} to dynamo")
        dynamo_repo.create_user(user)
        count += 1

    print(f"{count} users loaded to dynamo!")

    count = 0
    for transaction in mock_repo.transactions:
        print(f"Loading transaction {transaction.tran_id} for user {transaction.user_id}")
        dynamo_repo.create_transaction(transaction)
        count += 1

    print(f"{count} transactions loaded to dynamo!")

    count = 0
    for subscription in mock_repo.subscriptions:
        print(f"Loading subscription {subscription.sub_id} for user {subscription.user_id}")
        dynamo_repo.create_subscription(subscription)
        count += 1

    print(f"{count} subscriptions loaded to dynamo!")

    count = 0
    for kb in mock_repo.kbs:
        print(f"Loading knowledge base {kb.id}")
        dynamo_repo.create_knowledge_base(user_id="fdddafb9-687a-4982-a025-54fb12671932", kb=kb)
        count += 1

    print(f"{count} knowledge bases loaded to dynamo!")

def load_mock_to_real_dynamo():
    mock_repo = UserRepositoryMock()
    dynamo_repo = UserRepositoryDynamo()

    count = 0

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamo_table_name=Environments.get_envs().dynamo_table_name)

    print("Adding counter to table")

    table.put_item(
        Item={
            'PK': 'COUNTER',
            'SK': 'COUNTER',
            'COUNTER': Decimal(0)
        }
    )

    print('Loading mock data to dynamo...')
    for user in mock_repo.users:
        print(f"Loading user {user.user_id} | {user.name} to dynamo")
        dynamo_repo.create_user(user)
        count += 1

    print(f"{count} users loaded to dynamo!")
    
if __name__ == '__main__':
    dotenv.load_dotenv()
    load_mock_to_local_dynamo()
