import os
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from src.shared.domain.entities.knowledge_base import KnowledgeBase
from src.shared.domain.entities.kb_key import KbKey
from src.shared.domain.enums.status_enum import Status
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.keys_repository_interface import IKeysRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    ExternalServiceError,
    InfrastructureError,
    DatabaseError,
    ConfigurationError
)

envs = Environments.get_envs()

EMBEDDING_MODEL_ARN = envs.embedding_model_arn
RDS_CLUSTER_ARN = envs.rds_cluster_arn
RDS_SECRET_ARN = envs.rds_secret_arn
BEDROCK_ROLE_ARN = envs.bedrock_role_arn

DATABASE_NAME = "postgres"
VECTOR_FIELD = "embedding"
TEXT_FIELD = "chunks"
METADATA_FIELD = "metadata"
PK_FIELD = "id"

bedrock = boto3.client(
    "bedrock-agent",
    region_name=envs.region
)

rds_data = boto3.client(
    "rds-data",
    region_name=envs.region
)


class CreateKbUseCase:
    def __init__(self, repo: IUserRepository, keys_repo: IKeysRepository):
        self._validate_configuration()
        self.user_repository = repo
        self.keys_repository = keys_repo

    def _validate_configuration(self):
        required_env_vars = [
            "RDS_CLUSTER_ARN",
            "RDS_SECRET_ARN",
            "BEDROCK_ROLE_ARN"
        ]
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        if missing_vars:
            raise ConfigurationError(
                f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}"
            )

    def _generate_api_key(self) -> str:
        """Gera uma chave de API segura no formato knowly_{UUIDv4}"""
        uuid_key = str(uuid.uuid4())
        return f"knowly_{uuid_key}"

    def _create_kb(self, kb_name: str, kb_description: str, kb_display_name: str, user_id: str) -> tuple[str, str]:
        """
        Cria a KB e retorna uma tupla (kb_id, kb_key)
        """
        embedding_id = uuid.uuid4().hex
        table_name = f"kb.embedding_{embedding_id}"
        safe_suffix = table_name.split(".", 1)[1]
        gin_idx = f"{safe_suffix}_chunks_gin_idx"
        hnsw_idx = f"{safe_suffix}_embedding_hnsw_idx"
        kb_id = None

        try:
            self._create_rds_table(table_name, gin_idx, hnsw_idx)
            kb_id = self._create_bedrock_kb(kb_name, kb_description, table_name, user_id)
            self._persist_kb(
                user_id=user_id,
                kb_id=kb_id,
                kb_name=kb_name,
                kb_description=kb_description,
                kb_display_name=kb_display_name,
                rds_table=f"embedding_{embedding_id}"
            )

            # Criar chave de API após sucesso da KB
            kb_key = self._generate_api_key()
            kb_key_entity = KbKey(
                user_id=user_id,
                kb_id=kb_id,
                kb_key=kb_key,
                kb_key_alias=f"{kb_display_name} - Primary Key"
            )
            self.keys_repository.create_kb_key(kb_key_entity)

            return kb_id, kb_key

        except Exception:
            try:
                self._cleanup_failed_creation(table_name, kb_id)
            except:  # noqa
                pass
            raise

    def _persist_kb(self, user_id: str, kb_id: str, kb_name: str, kb_description: str, kb_display_name: str, rds_table: str):
        now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
        kb_entity = KnowledgeBase(
            id=kb_id,
            name=kb_name,
            description=kb_description or "",
            created_at=now_iso,
            updated_at=now_iso,
            status=Status.ACTIVE.value,
            documents_count=0,
            categories=[],
            display_name=kb_display_name or kb_name,
            rds_table=rds_table,
        )
        self.user_repository.create_knowledge_base(user_id=user_id, kb=kb_entity)

    def _create_rds_table(self, table_name: str, gin_idx: str, hnsw_idx: str):
        try:
            create_sql = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id uuid PRIMARY KEY,
                    embedding vector(1024),
                    chunks text,
                    metadata jsonb
                );
            """
            rds_data.execute_statement(
                resourceArn=RDS_CLUSTER_ARN,
                secretArn=RDS_SECRET_ARN,
                database=DATABASE_NAME,
                sql=create_sql
            )
            create_gin_sql = f"""
                CREATE INDEX IF NOT EXISTS {gin_idx}
                ON {table_name}
                USING gin (to_tsvector('simple', {TEXT_FIELD}));
            """
            rds_data.execute_statement(
                resourceArn=RDS_CLUSTER_ARN,
                secretArn=RDS_SECRET_ARN,
                database=DATABASE_NAME,
                sql=create_gin_sql
            )
            create_hnsw_sql = f"""
                CREATE INDEX IF NOT EXISTS {hnsw_idx}
                ON {table_name}
                USING hnsw ({VECTOR_FIELD} vector_cosine_ops);
            """
            rds_data.execute_statement(
                resourceArn=RDS_CLUSTER_ARN,
                secretArn=RDS_SECRET_ARN,
                database=DATABASE_NAME,
                sql=create_hnsw_sql
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'BadRequestException':
                raise DatabaseError(
                    f"Erro na sintaxe SQL ou estrutura da tabela: {e.response['Error']['Message']}"
                )
            if error_code == 'ForbiddenException':
                raise DatabaseError("Permissões insuficientes para criar tabela no RDS")
            print(e)
            raise DatabaseError(f"Erro ao criar tabela no RDS: {e.response['Error']['Message']}")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com RDS: {str(e)}")

    def _create_bedrock_kb(self, kb_name: str, kb_description: str, table_name: str, user_id: str) -> str:
        try:
            resp_kb = bedrock.create_knowledge_base(
                clientToken=str(uuid.uuid4()),
                name=kb_name,
                description=kb_description,
                roleArn=BEDROCK_ROLE_ARN,
                knowledgeBaseConfiguration={
                    "type": "VECTOR",
                    "vectorKnowledgeBaseConfiguration": {
                        "embeddingModelArn": EMBEDDING_MODEL_ARN
                    },
                },
                storageConfiguration={
                    "rdsConfiguration": {
                        "resourceArn": RDS_CLUSTER_ARN,
                        "credentialsSecretArn": RDS_SECRET_ARN,
                        "databaseName": DATABASE_NAME,
                        "tableName": table_name,
                        "fieldMapping": {
                            "vectorField": VECTOR_FIELD,
                            "textField": TEXT_FIELD,
                            "metadataField": METADATA_FIELD,
                            "primaryKeyField": PK_FIELD,
                        },
                    },
                    "type": "RDS",
                },
                tags={
                    "user_id": user_id
                }
            )
            return resp_kb["knowledgeBase"]["knowledgeBaseId"]
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ConflictException':
                raise DuplicatedItem(f"base de conhecimento com nome '{kb_name}'")
            if error_code == 'ValidationException':
                raise ExternalServiceError(
                    "Bedrock", f"Dados inválidos: {e.response['Error']['Message']}"
                )
            if error_code == 'ServiceQuotaExceededException':
                raise ExternalServiceError("Bedrock", "Cota de bases de conhecimento excedida")
            if error_code == 'AccessDeniedException':
                raise ExternalServiceError("Bedrock", "Acesso negado ao criar base de conhecimento")
            raise ExternalServiceError(
                "Bedrock", f"Erro ao criar knowledge base: {e.response['Error']['Message']}"
            )
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com Bedrock: {str(e)}")

    def _cleanup_failed_creation(self, table_name: str, kb_id: str = None):
        """Limpa recursos criados em caso de falha"""
        try:
            drop_sql = f"DROP TABLE IF EXISTS {table_name};"
            rds_data.execute_statement(
                resourceArn=RDS_CLUSTER_ARN,
                secretArn=RDS_SECRET_ARN,
                database=DATABASE_NAME,
                sql=drop_sql
            )
        except:  # noqa
            pass

        # Tentar deletar a KB do Bedrock se foi criada
        if kb_id:
            try:
                bedrock.delete_knowledge_base(knowledgeBaseId=kb_id)
            except:  # noqa
                pass

    def __call__(self, kb_name: str, kb_description: str, kb_display_name: str, user_id: str) -> tuple[str, str]:
        """
        Retorna uma tupla (kb_id, kb_key)
        """
        kb_id, kb_key = self._create_kb(kb_name, kb_description, kb_display_name, user_id)
        return kb_id, kb_key
