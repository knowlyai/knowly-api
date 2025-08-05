from dotenv import load_dotenv
import os
import uuid
import boto3
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.domain.enums.status_enum import Status
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    ExternalServiceError,
    InfrastructureError,
    DatabaseError,
    ConfigurationError
)

load_dotenv()

EMBEDDING_MODEL_ARN = os.environ.get(
    "EMBEDDING_MODEL_ARN",
    "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v2:0",
)
RDS_CLUSTER_ARN = os.environ["RDS_CLUSTER_ARN"]
RDS_SECRET_ARN = os.environ["RDS_SECRET_ARN"]
BEDROCK_ROLE_ARN = os.environ["BEDROCK_ROLE_ARN"]
DATABASE_NAME = "postgres"
VECTOR_FIELD = "embedding"
TEXT_FIELD = "chunks"
METADATA_FIELD = "metadata"
PK_FIELD = "id"

bedrock = boto3.client(
    "bedrock-agent",
    region_name=os.getenv("AWS_REGION_NAME")
)

rds_data = boto3.client(
    "rds-data",
    region_name=os.getenv("AWS_REGION_NAME")
)

ddb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION_NAME")
)
table = ddb.Table(
    os.getenv("DYNAMODB_TABLE_NAME")
)


class CreateKbUseCase:
    def __init__(self):
        self._validate_configuration()

    def _validate_configuration(self):
        """Valida se todas as configurações necessárias estão presentes"""
        required_env_vars = [
            "RDS_CLUSTER_ARN",
            "RDS_SECRET_ARN",
            "BEDROCK_ROLE_ARN",
            "AWS_REGION_NAME",
            "DYNAMODB_TABLE_NAME"
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def _kb_already_exists(self, name: str) -> bool:
        """Retorna True se a KB já existir"""
        try:
            paginator = bedrock.get_paginator("list_knowledge_bases")
            for page in paginator.paginate():
                for kb in page["knowledgeBaseSummaries"]:
                    if kb["name"] == name:
                        return True
            return False
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                raise ExternalServiceError("Bedrock", "Acesso negado ao listar bases de conhecimento")
            elif error_code == 'ThrottlingException':
                raise ExternalServiceError("Bedrock", "Limite de requisições excedido")
            else:
                raise ExternalServiceError("Bedrock", f"Erro ao listar bases de conhecimento: {e.response['Error']['Message']}")
        except NoCredentialsError:
            raise ConfigurationError("Credenciais AWS não encontradas")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com AWS: {str(e)}")

    def _create_kb(self, kb_name: str, kb_description: str) -> str:
        """Cria a base de conhecimento e retorna o ID"""
        embedding_id = uuid.uuid4().hex
        table_name = f"kb.embedding_{embedding_id}"
        safe_suffix = table_name.split(".", 1)[1]
        gin_idx = f"{safe_suffix}_chunks_gin_idx"
        hnsw_idx = f"{safe_suffix}_embedding_hnsw_idx"

        try:
            # Criar tabela no RDS
            self._create_rds_table(table_name, gin_idx, hnsw_idx)

            # Criar knowledge base no Bedrock
            kb_id = self._create_bedrock_kb(kb_name, kb_description, table_name)

            # Salvar no DynamoDB
            self._save_to_dynamodb(kb_id, embedding_id, kb_name, kb_description)

            return kb_id

        except Exception as e:
            # Em caso de erro, tentar fazer cleanup
            try:
                self._cleanup_failed_creation(table_name)
            except:
                pass  # Ignore cleanup errors
            raise

    def _create_rds_table(self, table_name: str, gin_idx: str, hnsw_idx: str):
        """Cria a tabela no RDS com tratamento de erros"""
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

            # Criar índices
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
                raise DatabaseError(f"Erro na sintaxe SQL ou estrutura da tabela: {e.response['Error']['Message']}")
            elif error_code == 'ForbiddenException':
                raise DatabaseError("Permissões insuficientes para criar tabela no RDS")
            else:
                raise DatabaseError(f"Erro ao criar tabela no RDS: {e.response['Error']['Message']}")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com RDS: {str(e)}")

    def _create_bedrock_kb(self, kb_name: str, kb_description: str, table_name: str) -> str:
        """Cria a knowledge base no Bedrock"""
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
                    "user_id": "inserir aqui"
                }
            )

            return resp_kb["knowledgeBase"]["knowledgeBaseId"]

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ConflictException':
                raise DuplicatedItem(f"base de conhecimento com nome '{kb_name}'")
            elif error_code == 'ValidationException':
                raise ExternalServiceError("Bedrock", f"Dados inválidos: {e.response['Error']['Message']}")
            elif error_code == 'ServiceQuotaExceededException':
                raise ExternalServiceError("Bedrock", "Cota de bases de conhecimento excedida")
            elif error_code == 'AccessDeniedException':
                raise ExternalServiceError("Bedrock", "Acesso negado ao criar base de conhecimento")
            else:
                raise ExternalServiceError("Bedrock", f"Erro ao criar knowledge base: {e.response['Error']['Message']}")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com Bedrock: {str(e)}")

    def _save_to_dynamodb(self, kb_id: str, embedding_id: str, kb_name: str, kb_description: str):
        """Salva os dados no DynamoDB"""
        try:
            table.put_item(
                Item={
                    "kb_id": kb_id,
                    "rds_table": f"embedding_{embedding_id}",
                    "user_id": "inserir aqui",
                    "name": kb_name,
                    "description": kb_description,
                    "status": Status.ACTIVE.value,
                    "created_at": int(datetime.now().timestamp()),
                    "updated_at": int(datetime.now().timestamp())
                }
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ConditionalCheckFailedException':
                raise DuplicatedItem(f"base de conhecimento com ID '{kb_id}'")
            elif error_code == 'ValidationException':
                raise DatabaseError(f"Dados inválidos para DynamoDB: {e.response['Error']['Message']}")
            else:
                raise DatabaseError(f"Erro ao salvar no DynamoDB: {e.response['Error']['Message']}")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com DynamoDB: {str(e)}")

    def _cleanup_failed_creation(self, table_name: str):
        """Limpa recursos criados em caso de falha"""
        try:
            drop_sql = f"DROP TABLE IF EXISTS {table_name};"
            rds_data.execute_statement(
                resourceArn=RDS_CLUSTER_ARN,
                secretArn=RDS_SECRET_ARN,
                database=DATABASE_NAME,
                sql=drop_sql
            )
        except:
            pass  # Ignore cleanup errors

    def __call__(self, kb_name: str, kb_description: str) -> str:
        """Executa o caso de uso de criação de knowledge base"""
        try:
            # Verificar se já existe
            if self._kb_already_exists(kb_name):
                raise DuplicatedItem(f"base de conhecimento com nome '{kb_name}'")

            # Criar a knowledge base
            kb_id = self._create_kb(kb_name, kb_description)
            return kb_id

        except (DuplicatedItem, ExternalServiceError, InfrastructureError,
                DatabaseError, ConfigurationError) as e:
            # Re-raise domain errors as-is
            raise e
        except Exception as e:
            # Wrap unexpected errors
            raise InfrastructureError(f"Erro inesperado ao criar base de conhecimento: {str(e)}")
