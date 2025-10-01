import os
import uuid

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)


bedrock = boto3.client(
    "bedrock-agent",
    region_name=os.getenv('REGION')
)


class SyncKbUseCase:
    def __init__(self):
        self._validate_configuration()

    def _validate_configuration(self):
        """Valida se todas as configurações necessárias estão presentes"""
        required_env_vars = [
            "REGION"
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def _get_ds_name(self, kb_id: str) -> str:
        return f"s3-ds-{kb_id}"

    def _create_or_get_data_source(self, bucket_name: str, user_id: str, kb_id: str) -> str:
        """Cria ou obtém uma fonte de dados para a knowledge base"""
        try:
            bucket_arn = f"arn:aws:s3:::{bucket_name}"
            ds_name = f"s3-ds-{kb_id}"
            prefix = f"{user_id}/{kb_id}"

            # Verificar se o data source já existe
            for page in bedrock.get_paginator("list_data_sources").paginate(knowledgeBaseId=kb_id):
                for ds in page["dataSourceSummaries"]:
                    if ds["name"] == ds_name:
                        return ds["dataSourceId"]

            # Criar novo data source
            resp = bedrock.create_data_source(
                clientToken=str(uuid.uuid4()),
                knowledgeBaseId=kb_id,
                name=ds_name,
                description="Arquivos enviados pelo usuário via prefixo S3",
                dataSourceConfiguration={
                    "type": "S3",
                    "s3Configuration": {
                        "bucketArn": bucket_arn,
                        "inclusionPrefixes": [prefix]
                    },
                },
                vectorIngestionConfiguration={
                    "chunkingConfiguration": {
                        "chunkingStrategy": "SEMANTIC",
                        "fixedSizeChunkingConfiguration": {
                            "maxTokens": 800,
                            "overlapPercentage": 20
                        },
                        "semanticChunkingConfiguration": {
                            "breakpointPercentileThreshold": 95,
                            "bufferSize": 1,
                            "maxTokens": 800
                        }
                    }
                }
            )
            return resp["dataSource"]["dataSourceId"]

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                if 'knowledgeBase' in e.response['Error']['Message']:
                    raise NoItemsFound(f"base de conhecimento com ID '{kb_id}'")
                else:
                    raise ExternalServiceError("Bedrock", f"Recurso não encontrado: {e.response['Error']['Message']}")
            elif error_code == 'AccessDeniedException':
                raise ExternalServiceError("Bedrock", "Acesso negado ao gerenciar fonte de dados")
            elif error_code == 'ValidationException':
                raise ExternalServiceError("Bedrock", f"Dados inválidos: {e.response['Error']['Message']}")
            elif error_code == 'ConflictException':
                raise ExternalServiceError("Bedrock", f"Conflito ao criar fonte de dados: {e.response['Error']['Message']}")
            else:
                raise ExternalServiceError("Bedrock", f"Erro ao gerenciar fonte de dados: {e.response['Error']['Message']}")
        except NoCredentialsError:
            raise ConfigurationError("Credenciais AWS não encontradas")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com Bedrock: {str(e)}")

    def _start_ingestion_and_wait(self, kb_id: str, ds_id: str) -> str:
        """Inicia o job de ingestão de dados"""
        try:
            job = bedrock.start_ingestion_job(
                clientToken=str(uuid.uuid4()),
                knowledgeBaseId=kb_id,
                dataSourceId=ds_id,
            )["ingestionJob"]

            job_id = job["ingestionJobId"]
            return f"Job {job_id} iniciado com sucesso"

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                raise NoItemsFound(f"fonte de dados com ID '{ds_id}' ou base de conhecimento com ID '{kb_id}'")
            elif error_code == 'ConflictException':
                raise ExternalServiceError("Bedrock", "Já existe um job de ingestão em execução para esta fonte de dados")
            elif error_code == 'AccessDeniedException':
                raise ExternalServiceError("Bedrock", "Acesso negado para iniciar job de ingestão")
            elif error_code == 'ServiceQuotaExceededException':
                raise ExternalServiceError("Bedrock", "Limite de jobs de ingestão simultâneos excedido")
            else:
                raise ExternalServiceError("Bedrock", f"Erro ao iniciar job de ingestão: {e.response['Error']['Message']}")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com Bedrock: {str(e)}")

    def __call__(self, bucket_name: str, user_id: str, kb_id: str) -> str:
        """Executa a sincronização da base de conhecimento"""
        try:
            ds_id = self._create_or_get_data_source(bucket_name, user_id, kb_id)
            response = self._start_ingestion_and_wait(kb_id, ds_id)
            return response

        except (NoItemsFound, ExternalServiceError, InfrastructureError, ConfigurationError) as e:
            # Re-raise domain errors as-is
            raise e
        except Exception as e:
            # Wrap unexpected errors
            raise InfrastructureError(f"Erro inesperado ao sincronizar base de conhecimento: {str(e)}")
