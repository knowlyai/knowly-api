import os

from aws_cdk import (
    aws_dynamodb as dynamodb, RemovalPolicy, CfnOutput,
)
from constructs import Construct


class DynamoStack(Construct):
    table: dynamodb.Table
    keys_table: dynamodb.Table

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope, "KnowlyDynamo")

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")

        removal_policy = RemovalPolicy.RETAIN if 'prod' in self.github_ref_name else RemovalPolicy.DESTROY

        self.table = dynamodb.Table(
            self, "KnowlyApiDynamoTable",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING,
            ),
            point_in_time_recovery=True,
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy
        )
        CfnOutput(self, 'DynamoKnowlyRemovalPolicy', value=removal_policy.value, export_name=f'Knowly{self.github_ref_name}DynamoKnowlyRemovalPolicyValue')

        self.keys_table = dynamodb.Table(
            self, "KnowlyKeysDynamoTable",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING,
            ),
            point_in_time_recovery=True,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=removal_policy
        )

        self.keys_table.add_global_secondary_index(
            index_name="GSI1",
            partition_key=dynamodb.Attribute(
                name="GSI1PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="GSI1SK",
                type=dynamodb.AttributeType.STRING
            )
        )





