import os

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.usecase_errors import (
    ConfigurationError,
    ExternalServiceError,
    InfrastructureError
)
from .generate_presigned_bucket_url import generate_presigned_bucket_url
from .types import PresignedPostResponse


class GetPresignedBucketUrlUseCase:
    def __init__(self, repo: IUserRepository):
        self._validate_configuration()
        self.repo = repo

    def _validate_configuration(self):
        """Valida se todas as configurações necessárias estão presentes"""
        required_env_vars = [
            "AWS_REGION_NAME"
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            raise ConfigurationError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}")

    def _validate_parameters(self, bucket: str, user_id: str, kb_id: str, expires: int, max_size_mb: int):
        """Valida os parâmetros de entrada"""
        if expires <= 0:
            raise ValueError("Tempo de expiração deve ser maior que zero")

        if expires > 604800:  # 7 dias em segundos
            raise ValueError("Tempo de expiração não pode ser maior que 7 dias (604800 segundos)")

        if max_size_mb <= 0:
            raise ValueError("Tamanho máximo deve ser maior que zero")

        if max_size_mb > 5120:  # 5GB
            raise ValueError("Tamanho máximo não pode ser maior que 5GB (5120 MB)")

    def __call__(self, bucket: str, user_id: str, kb_id: str, expires: int = 900, max_size_mb: int = 20) -> PresignedPostResponse:
        try:
            # Validar parâmetros
            self._validate_parameters(bucket, user_id, kb_id, expires, max_size_mb)

            # Gerar URL pré-assinada
            return generate_presigned_bucket_url(
                bucket=bucket,
                prefix=f"{user_id}/{kb_id}/",
                expires=expires,
                max_size_mb=max_size_mb
            )

        except ValueError as e:
            # Re-raise validation errors as-is
            raise e
        except (ConfigurationError, ExternalServiceError, InfrastructureError) as e:
            # Re-raise domain errors as-is
            raise e
        except Exception as e:
            # Wrap unexpected errors
            raise InfrastructureError(f"Erro inesperado ao gerar URL pré-assinada: {str(e)}")
