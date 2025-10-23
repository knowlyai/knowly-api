import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.repositories.keys_repository_interface import IKeysRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import (
    InfrastructureError,
    DatabaseError,
    ConfigurationError,
    ExternalServiceError,
    NoItemsFound
)

envs = Environments.get_envs()

class GetKbUseCase:
    def __init__(self, repo: IUserRepository, keys_repo: IKeysRepository):
        self.repo = repo
        self.keys_repo = keys_repo
        self._validate_configuration()
        self.s3 = boto3.client(
            "s3",
            region_name=os.getenv("AWS_REGION_NAME")
        )

    def _validate_configuration(self):
        required_env_vars = [
            "AWS_REGION_NAME"
        ]
        missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def get_knowledge_bases(self, user_id: str, kb_id: str = None):
        try:
            # Obtém lista de entidades KnowledgeBase (1 ou muitas) via repositório
            kbs = self.repo.get_knowledge_base(user_id=user_id, kb_id=kb_id)

            formatted = []
            for kb in kbs:
                files, total_size_mb = self._get_kb_files_and_size(user_id, kb.id)

                # Buscar chaves da KB
                kb_keys = []
                keys = self.keys_repo.get_kb_keys(user_id=user_id, kb_id=kb.id)
                kb_keys = [
                    {
                        "kb_key": key.kb_key,
                        "kb_key_alias": key.kb_key_alias
                    }
                    for key in keys
                ]

                if kb_keys is None:
                    kb_keys = []
                print(kb_keys)
                formatted.append({
                    "kb_id": kb.id,
                    "name": kb.name,
                    "display_name": kb.display_name,
                    "description": kb.description,
                    # Mantemos valores originais (podem ser ISO strings) para não forçar conversão incorreta
                    "created_at": kb.created_at,
                    "updated_at": kb.updated_at,
                    "status": kb.status,
                    "files": files,
                    "total_size_mb": total_size_mb,
                    "keys": kb_keys
                })

            return {"knowledge_bases": formatted}

        except NoItemsFound:
            # kb_id específico não encontrado -> retorna lista vazia para manter contrato anterior
            return {"knowledge_bases": []}
        except NoCredentialsError:
            raise ConfigurationError("Credenciais AWS não encontradas")
        except ClientError as e:
            # Erros de S3 tratados separadamente dentro do método de arquivos; aqui tratamos genérico
            raise ExternalServiceError("AWS", f"Erro ao acessar serviços AWS: {e.response['Error'].get('Message', 'erro desconhecido')}")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com AWS: {str(e)}")
        except DatabaseError:
            # Propaga se repositório já encapsular; manter assinatura
            raise

    def _get_kb_files_and_size(self, user_id: str, kb_id: str):
        try:
            bucket_name = envs.s3_bucket_name
            region = envs.region
            prefix = f"{user_id}/{kb_id}/"

            files = []
            total_size_bytes = 0

            paginator = self.s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

            for page in pages:
                if 'Contents' in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        size = obj['Size']
                        filename = key.replace(prefix, '')
                        import urllib.parse
                        encoded_filename = urllib.parse.quote(filename, safe='')
                        file_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{user_id}/{kb_id}/{encoded_filename}"
                        files.append({
                            "filename": filename,
                            "url": file_url,
                            "size_bytes": size
                        })
                        total_size_bytes += size

            total_size_mb = round(total_size_bytes / (1024 * 1024), 2)
            return files, total_size_mb

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                return [], 0.0
            elif error_code == 'AccessDenied':
                raise ExternalServiceError("S3", "Acesso negado ao listar arquivos do bucket S3")
            else:
                raise ExternalServiceError("S3", f"Erro ao listar arquivos do S3: {e.response['Error']['Message']}")
        except Exception:
            return [], 0.0
