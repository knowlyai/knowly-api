import os

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)

envs = Environments().get_envs()

s3 = boto3.client(
    "s3",
    region_name=envs.region
)

class DeleteKbFileUseCase:
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

    def _validate_parameters(self, bucket: str, user_id: str, kb_id: str, file_name: str):
        """Valida os parâmetros de entrada"""
        if '/' in file_name or '\\' in file_name:
            raise ValueError("Nome do arquivo não pode conter barras (/ ou \\)")

        if '..' in file_name:
            raise ValueError("Nome do arquivo não pode conter '..'")

        if len(file_name.strip()) > 255:
            raise ValueError("Nome do arquivo não pode ter mais que 255 caracteres")

    def __call__(self, bucket: str, user_id: str, kb_id: str, file_name: str) -> str:
        """Deleta um arquivo do S3 no caminho user_id/kb_id/file_name"""
        try:
            # Validar parâmetros
            self._validate_parameters(bucket, user_id, kb_id, file_name)

            key = f"{user_id.strip()}/{kb_id.strip()}/{file_name.strip()}"

            # Verificar se o arquivo existe antes de tentar deletar
            try:
                s3.head_object(Bucket=bucket, Key=key)
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    raise NoItemsFound(f"arquivo '{file_name}' no caminho '{user_id}/{kb_id}'")
                else:
                    raise

            # Deletar o arquivo
            s3.delete_object(Bucket=bucket, Key=key)
            return f"Arquivo '{file_name}' deletado com sucesso"

        except ValueError as e:
            # Re-raise validation errors as-is
            raise e
        except NoItemsFound as e:
            # Re-raise not found errors as-is
            raise e
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchBucket':
                raise ExternalServiceError("S3", f"Bucket '{bucket}' não encontrado")
            elif error_code == 'AccessDenied':
                raise ExternalServiceError("S3", "Acesso negado ao deletar arquivo do bucket S3")
            elif error_code == 'InvalidBucketName':
                raise ExternalServiceError("S3", f"Nome do bucket '{bucket}' é inválido")
            else:
                raise ExternalServiceError("S3", f"Erro ao deletar arquivo: {e.response['Error']['Message']}")
        except NoCredentialsError:
            raise ConfigurationError("Credenciais AWS não encontradas")
        except BotoCoreError as e:
            raise InfrastructureError(f"Erro de conectividade com S3: {str(e)}")
        except (ConfigurationError, ExternalServiceError, InfrastructureError) as e:
            # Re-raise domain errors as-is
            raise e
        except Exception as e:
            # Wrap unexpected errors
            raise InfrastructureError(f"Erro inesperado ao deletar arquivo: {str(e)}")
