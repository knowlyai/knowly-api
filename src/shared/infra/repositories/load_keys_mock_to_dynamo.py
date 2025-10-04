import boto3
import dotenv

from src.shared.infra.repositories.keys_repository_dynamo import KeysRepositoryDynamo
from src.shared.infra.repositories.keys_repository_mock import KeysRepositoryMock


def setup_keys_dynamo_table():
    dynamo_table_name = "keys-table-test"
    endpoint_url = "http://localhost:8000"
    print("Setting up Keys DynamoDB table...")

    dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint_url, region_name='us-east-1')
    print("DynamoDB client created")
    tables = dynamo_client.list_tables()['TableNames']

    if dynamo_table_name not in tables:
        print("Creating keys table...")
        dynamo_client.create_table(
            TableName=dynamo_table_name,
            KeySchema=[
                {
                    'AttributeName': 'PK',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'PK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'GSI1PK',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'GSI1SK',
                    'AttributeType': 'S'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'GSI1',
                    'KeySchema': [
                        {
                            'AttributeName': 'GSI1PK',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'GSI1SK',
                            'KeyType': 'RANGE'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ],
            BillingMode='PAY_PER_REQUEST',
        )
        print("Waiting for table to be created...")
        dynamo_client.get_waiter('table_exists').wait(TableName=dynamo_table_name)

        print(f'Table "{dynamo_table_name}" created!')

    else:
        print("Keys table already exists!")


def load_keys_mock_to_local_dynamo():
    setup_keys_dynamo_table()
    mock_repo = KeysRepositoryMock()
    dynamo_repo = KeysRepositoryDynamo()

    count = 0

    print('Loading mock keys data to dynamo...')
    for kb_key in mock_repo.kb_keys:
        print(f"Loading key {kb_key.kb_key_alias} for user {kb_key.user_id} | KB {kb_key.kb_id}")
        dynamo_repo.create_kb_key(kb_key)
        count += 1

    print(f"{count} keys loaded to dynamo!")


def load_keys_mock_to_real_dynamo():
    mock_repo = KeysRepositoryMock()
    dynamo_repo = KeysRepositoryDynamo()

    count = 0

    print('Loading mock keys data to dynamo...')
    for kb_key in mock_repo.kb_keys:
        print(f"Loading key {kb_key.kb_key_alias} for user {kb_key.user_id} | KB {kb_key.kb_id}")
        dynamo_repo.create_kb_key(kb_key)
        count += 1

    print(f"{count} keys loaded to dynamo!")


if __name__ == '__main__':
    dotenv.load_dotenv()
    load_keys_mock_to_local_dynamo()
