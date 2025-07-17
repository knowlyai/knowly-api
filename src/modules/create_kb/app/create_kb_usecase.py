from dotenv import load_dotenv
import os
import uuid
import boto3

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
    region_name=os.getenv('AWS_REGION_NAME')
)

rds_data = boto3.client(
    "rds-data",
    region_name=os.getenv('AWS_REGION_NAME')
)


class CreateKbUseCase:
    @staticmethod
    def _kb_already_exists(name: str) -> bool:
        """Retorna o ID da KB se já existir"""
        paginator = bedrock.get_paginator("list_knowledge_bases")
        for page in paginator.paginate():
            for kb in page["knowledgeBaseSummaries"]:
                if kb["name"] == name:
                    return True
        return False

    @staticmethod
    def _create_kb(kb_name: str, kb_description: str) -> dict:
        kb_id = uuid.uuid4().hex
        table_name = f"kb.embedding_{kb_id}"
        safe_suffix = table_name.split('.', 1)[1]
        gin_idx = f"{safe_suffix}_chunks_gin_idx"
        hnsw_idx = f"{safe_suffix}_embedding_hnsw_idx"

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
        create_sql = f"""
            CREATE INDEX IF NOT EXISTS {gin_idx}
            ON {table_name}
            USING gin (to_tsvector('simple', {TEXT_FIELD}));
        """
        rds_data.execute_statement(
            resourceArn=RDS_CLUSTER_ARN,
            secretArn=RDS_SECRET_ARN,
            database=DATABASE_NAME,
            sql=create_sql
        )
        create_sql = f"""
            CREATE INDEX IF NOT EXISTS {hnsw_idx}
            ON {table_name}
            USING hnsw ({VECTOR_FIELD} vector_cosine_ops);
        """
        rds_data.execute_statement(
            resourceArn=RDS_CLUSTER_ARN,
            secretArn=RDS_SECRET_ARN,
            database=DATABASE_NAME,
            sql=create_sql
        )
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
        # Pegar o id da resp_kb e armazenar no Dynamo. Fazer a relação entre o id da KB e o id gerado
        return resp_kb["knowledgeBase"]["knowledgeBaseId"]

    def __call__(self, kb_name: str, kb_description: str):
        if self._kb_already_exists(kb_name):
            return "Knowledge Base already exists with this name."

        response = self._create_kb(kb_name, kb_description)
        return response
