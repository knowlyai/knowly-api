import os

from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    Duration, aws_cognito,
)
from aws_cdk.aws_apigateway import RestApi, Cors, LambdaIntegration
from constructs import Construct
from aws_cdk import aws_iam as iam

from .aurora_stack import AuroraStack
from .bucket_stack import BucketStack
from .cloudfront_stack import CloudFrontStack
from .cognito_stack import CognitoStack
from .dynamo_stack import DynamoStack
from .lambda_stack import LambdaStack


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.github_ref_name = os.environ.get("GITHUB_REF_NAME")
        self.aws_region = os.environ.get("AWS_REGION")
        stage = self.github_ref_name

        # API Gateway principal
        self.rest_api = RestApi(self, "KnowlyRestApi",
                                rest_api_name="KnowlyRestApi",
                                description=f"This is the Knowly RestApi for {self.github_ref_name}",
                                default_cors_preflight_options=
                                {
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
                                    "allow_headers": ["*"]
                                },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("knowly-api", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
                                                               )

        # API Gateway separado para Chat (público)
        self.chat_api = RestApi(self, "KnowlyChatApi",
                                rest_api_name="KnowlyChatApi",
                                description=f"This is the Knowly Chat Public API for {self.github_ref_name}",
                                default_cors_preflight_options=
                                {
                                    "allow_origins": Cors.ALL_ORIGINS,
                                    "allow_methods": ["POST", "OPTIONS"],
                                    "allow_headers": Cors.DEFAULT_HEADERS
                                },
                                )

        self.dynamo_table = DynamoStack(self)

        self.cognito_stack = CognitoStack(self, f'knowly_cognito_stack_{self.github_ref_name}')

        # Bucket S3 deve ser criado primeiro
        self.bucket_stack = BucketStack(self, f'knowly_bucket_stack_{self.github_ref_name}', stage=stage)

        # CloudFront Distribution para acesso aos arquivos do S3
        self.cloudfront_stack = CloudFrontStack(self, f'knowly_cloudfront_stack_{self.github_ref_name}',
                                                bucket=self.bucket_stack.bucket,
                                                stage=stage)

        # Stack de acesso ao S3
        self.s3_access_stack = S3AccessStack(self, f'knowly_s3_access_stack_{self.github_ref_name}',
                                             bucket=self.bucket_stack.bucket)

        self.aurora_stack = AuroraStack(self, f'knowly_aurora_stack_{self.github_ref_name}', env=kwargs.get('env'))

        custom_message_function = lambda_.Function(
            self, "CustomMessageFunction",
            code=lambda_.Code.from_asset("iac"),
            memory_size=128,
            handler="send_email.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            timeout=Duration.seconds(15),
        )

        self.cognito_stack.user_pool.add_trigger(
            aws_cognito.UserPoolOperation.CUSTOM_MESSAGE,
            custom_message_function
        )

        # Recupera variáveis opcionais para Bedrock / embedding
        bedrock_role_arn = os.environ.get("BEDROCK_ROLE_ARN")
        embedding_model_arn = os.environ.get("EMBEDDING_MODEL_ARN")

        ENVIRONMENT_VARIABLES = {
            "STAGE": stage,
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "DYNAMO_KEYS_TABLE_NAME": self.dynamo_table.keys_table.table_name,
            "DYNAMO_KEYS_PARTITION_KEY": "PK",
            "DYNAMO_KEYS_GSI1_NAME": "GSI1",
            "DYNAMO_KEYS_GSI1_PARTITION_KEY": "GSI1PK",
            "DYNAMO_KEYS_GSI1_SORT_KEY": "GSI1SK",
            "REGION": self.region,
            "AWS_REGION_NAME": self.region,
            "COGNITO_CLIENT_ID": self.cognito_stack.client.user_pool_client_id,
            "S3_BUCKET_NAME": self.bucket_stack.bucket_name,
            "S3_BUCKET_ARN": self.bucket_stack.bucket_arn,
            "CLOUDFRONT_DOMAIN_NAME": self.cloudfront_stack.distribution_domain_name,
            "CLOUDFRONT_DISTRIBUTION_ID": self.cloudfront_stack.distribution_id,
            "RDS_CLUSTER_ARN": self.aurora_stack.cluster_arn,
            "RDS_SECRET_ARN": self.aurora_stack.secret_arn,
        }

        if bedrock_role_arn:
            ENVIRONMENT_VARIABLES["BEDROCK_ROLE_ARN"] = bedrock_role_arn
        if embedding_model_arn:
            ENVIRONMENT_VARIABLES["EMBEDDING_MODEL_ARN"] = embedding_model_arn

        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES,
                                        user_pool=self.cognito_stack.user_pool,
                                        chat_api=self.chat_api)

        for function in self.lambda_stack.functions_that_need_dynamo_permissions:
            self.dynamo_table.table.grant_read_write_data(function)
            self.dynamo_table.keys_table.grant_read_write_data(function)

        # Permissões DynamoDB para a função chat (acesso à tabela de keys)
        if self.lambda_stack.chat_function:
            self.dynamo_table.keys_table.grant_read_write_data(self.lambda_stack.chat_function)

        # --- Permissões extras somente para a função create_kb ---
        create_kb_fn = self.lambda_stack.create_kb_function

        # RDS Data API (ExecuteStatement e opcionalmente BatchExecuteStatement)
        create_kb_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["rds-data:ExecuteStatement", "rds-data:BatchExecuteStatement"],
            resources=[self.aurora_stack.cluster_arn]
        ))

        # Secrets Manager para obter credenciais do cluster
        create_kb_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["secretsmanager:GetSecretValue"],
            resources=[self.aurora_stack.secret_arn]
        ))

        # Bedrock Knowledge Base actions
        create_kb_fn.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "bedrock:CreateKnowledgeBase",
                "bedrock:GetKnowledgeBase",
                "bedrock:TagResource",
                "bedrock:ListKnowledgeBases"
            ],
            resources=["*"]  # Ainda não existe a KB no deploy, usar wildcard
        ))

        # PassRole apenas se informado o BEDROCK_ROLE_ARN (requer condição PassedToService)
        if bedrock_role_arn:
            create_kb_fn.add_to_role_policy(iam.PolicyStatement(
                actions=["iam:PassRole"],
                resources=[bedrock_role_arn],
                conditions={"StringEquals": {"iam:PassedToService": "bedrock.amazonaws.com"}}
            ))

        # --- Permissões S3 para get_kb ---
        get_kb_fn = self.lambda_stack.get_kb_function
        get_kb_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:ListBucket"],
            resources=[self.bucket_stack.bucket_arn]
        ))
        get_kb_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{self.bucket_stack.bucket_arn}/*"]
        ))

        # --- Permissões S3 para get_presigned_bucket_url ---
        get_presigned_fn = self.lambda_stack.get_presigned_bucket_url_function
        get_presigned_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:PutObject"],
            resources=[f"{self.bucket_stack.bucket_arn}/*"]
        ))

        # --- Permissões S3 para delete_kb_file ---
        delete_kb_file_fn = self.lambda_stack.delete_kb_file_function
        delete_kb_file_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:DeleteObject"],
            resources=[f"{self.bucket_stack.bucket_arn}/*"]
        ))

        # --- Permissões Bedrock para sync_kb ---
        sync_kb_fn = self.lambda_stack.sync_kb_function
        sync_kb_fn.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "bedrock:ListDataSources",
                "bedrock:CreateDataSource",
                "bedrock:StartIngestionJob"
            ],
            resources=["*"]
        ))

        # --- Permissões Bedrock Runtime para chat ---
        if self.lambda_stack.chat_function:
            self.lambda_stack.chat_function.add_to_role_policy(iam.PolicyStatement(
                actions=[
                    "bedrock:RetrieveAndGenerate",
                    "bedrock:Retrieve",
                    "bedrock:InvokeModel"
                ],
                resources=["*"]
            ))
