import os
from enum import Enum

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.keys_repository_interface import IKeysRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly. Please use Environments.get_envs() method instead.

    Usage:

    """
    stage: STAGE
    s3_bucket_name: str
    region: str
    endpoint_url: str = None
    dynamo_table_name: str
    dynamo_partition_key: str
    dynamo_sort_key: str
    dynamo_keys_table_name: str
    dynamo_keys_partition_key: str
    dynamo_keys_gsi1_name: str
    dynamo_keys_gsi1_partition_key: str
    dynamo_keys_gsi1_sort_key: str
    mss_name: str
    rds_cluster_arn: str
    rds_secret_arn: str
    s3_bucket_arn: str
    s3_bucket_name: str
    bedrock_role_arn: str
    embedding_model_arn: str

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.DOTENV.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        # Corrigindo: converter para maiúsculo para corresponder ao enum
        stage_value = os.environ.get("STAGE", "").upper()
        self.stage = STAGE[stage_value]
        self.mss_name = os.environ.get("MSS_NAME")
        
        if self.stage == STAGE.TEST:
            self.s3_bucket_name = "bucket-test"
            self.region = "sa-east-1"
            self.endpoint_url = "http://localhost:8000"
            self.dynamo_table_name = "user_mss_template-table"
            self.dynamo_partition_key = "PK"
            self.dynamo_sort_key = "SK"
            self.dynamo_keys_table_name = "keys-table-test"
            self.dynamo_keys_partition_key = "PK"
            self.dynamo_keys_gsi1_name = "GSI1"
            self.dynamo_keys_gsi1_partition_key = "GSI1PK"
            self.dynamo_keys_gsi1_sort_key = "GSI1SK"

        else:
            self.region = os.environ.get("REGION")
            self.endpoint_url = os.environ.get("ENDPOINT_URL")
            self.dynamo_table_name = os.environ.get("DYNAMO_TABLE_NAME")
            self.dynamo_partition_key = os.environ.get("DYNAMO_PARTITION_KEY")
            self.dynamo_sort_key = os.environ.get("DYNAMO_SORT_KEY")
            self.dynamo_keys_table_name = os.environ.get("DYNAMO_KEYS_TABLE_NAME")
            self.dynamo_keys_partition_key = os.environ.get("DYNAMO_KEYS_PARTITION_KEY")
            self.dynamo_keys_gsi1_name = os.environ.get("DYNAMO_KEYS_GSI1_NAME")
            self.dynamo_keys_gsi1_partition_key = os.environ.get("DYNAMO_KEYS_GSI1_PARTITION_KEY")
            self.dynamo_keys_gsi1_sort_key = os.environ.get("DYNAMO_KEYS_GSI1_SORT_KEY")
            self.rds_cluster_arn = os.environ.get("RDS_CLUSTER_ARN")
            self.rds_secret_arn = os.environ.get("RDS_SECRET_ARN")
            self.s3_bucket_arn = os.environ.get("S3_BUCKET_ARN")
            self.s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
            self.bedrock_role_arn = os.environ.get("BEDROCK_ROLE_ARN")
            self.embedding_model_arn = os.environ.get("EMBEDDING_MODEL_ARN")



    @staticmethod
    def get_user_repo() -> IUserRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
            return UserRepositoryMock()
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo
            return UserRepositoryDynamo()
        else:
            raise Exception("No repository found for this stage")

    @staticmethod
    def get_keys_repo() -> IKeysRepository:
        if Environments.get_envs().stage == STAGE.TEST:
            from src.shared.infra.repositories.keys_repository_mock import KeysRepositoryMock
            return KeysRepositoryMock()
        elif Environments.get_envs().stage in [STAGE.DEV, STAGE.HOMOLOG, STAGE.PROD]:
            from src.shared.infra.repositories.keys_repository_dynamo import KeysRepositoryDynamo
            return KeysRepositoryDynamo()
        else:
            raise Exception("No repository found for this stage")

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object instead of instantiating it directly.
        :return: Environments (stage={self.stage}, s3_bucket_name={self.s3_bucket_name}, region={self.region}, endpoint_url={self.endpoint_url})

        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return self.__dict__
