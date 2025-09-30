import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError

from .types import PresignedPostResponse
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError
)

envs = Environments.get_envs()

s3 = boto3.client(
    's3',
    region_name=envs.region,
)


def generate_presigned_bucket_url(
        bucket: str,
        prefix: str,
        expires: int = 900,
        max_size_mb: int = 20
) -> PresignedPostResponse:
    try:
        response = s3.generate_presigned_post(
            Bucket=bucket,
            Key=f"{prefix.rstrip('/')}/${{filename}}",
            ExpiresIn=expires,
            Conditions=[
                ["starts-with", "$key", prefix],
                ["content-length-range", 1, max_size_mb * 1024 * 1024]
            ]
        )
        return response

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchBucket':
            raise ExternalServiceError("S3", f"Bucket '{bucket}' não encontrado")
        elif error_code == 'AccessDenied':
            raise ExternalServiceError("S3", "Acesso negado ao bucket S3")
        elif error_code == 'InvalidBucketName':
            raise ExternalServiceError("S3", f"Nome do bucket '{bucket}' é inválido")
        else:
            raise ExternalServiceError("S3", f"Erro ao gerar URL pré-assinada: {e.response['Error']['Message']}")
    except NoCredentialsError:
        raise ConfigurationError("Credenciais AWS não encontradas")
    except BotoCoreError as e:
        raise InfrastructureError(f"Erro de conectividade com S3: {str(e)}")
    except Exception as e:
        raise InfrastructureError(f"Erro inesperado ao gerar URL: {str(e)}")
