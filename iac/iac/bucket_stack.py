from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy
)
from constructs import Construct

class BucketStack(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, stage: str = "TEST", **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucket = s3.Bucket(
            self, "knowly-knowledge-bases-bucket",
            bucket_name=f"knowly-knowledge-bases-files-{stage}",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        self.bucket.add_cors_rule(
            allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.PUT, s3.HttpMethods.POST, s3.HttpMethods.HEAD],
            allowed_origins=[
                "https://dev.knowly.dev.br",
                "https://hml.knowly.dev.br",
                "https://knowly.dev.br",
                "http://localhost:3000"],
            allowed_headers=["*"],
            exposed_headers=["ETag"],
            max_age= 3000
        )

        # Role que o Bedrock vai assumir para ler o S3 (requerido!)
        self.kb_role = iam.Role(
            self, "BedrockKbExecutionRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            description="Exec role for Bedrock Knowledge Base to read S3 data source"
        )

        # Permissões de leitura (identidade) – suficiente em mesma conta
        self.bucket.grant_read(self.kb_role)

        self.bucket_name = self.bucket.bucket_name
        self.bucket_arn = self.bucket.bucket_arn