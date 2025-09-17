from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase
from src.modules.get_presigned_bucket_url.app.types import GetPresignedBucketUrlRequest
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError, BadRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError
)
from src.shared.infra.dto.user_api_gateway_dto import UserApiGatewayDTO


class GetPresignedBucketUrlController:
    def __init__(self, get_presigned_bucket_url_use_case: GetPresignedBucketUrlUseCase):
        self.get_presigned_bucket_url_use_case = get_presigned_bucket_url_use_case

    def _validate_parameters(self, bucket: str, user_id: str, kb_id: str, expires: int, max_size_mb: int):
        """Valida os parâmetros de entrada na controller"""
        if not bucket or not bucket.strip():
            raise ValueError("Nome do bucket é obrigatório")

        if not user_id or not user_id.strip():
            raise ValueError("ID do usuário é obrigatório")

        if not kb_id or not kb_id.strip():
            raise ValueError("ID da base de conhecimento é obrigatório")

        if len(bucket.strip()) < 3:
            raise ValueError("Nome do bucket deve ter pelo menos 3 caracteres")

        if len(user_id.strip()) < 1:
            raise ValueError("ID do usuário não pode estar vazio")

        if len(kb_id.strip()) < 1:
            raise ValueError("ID da base de conhecimento não pode estar vazio")

    def __call__(self, request: IRequest[GetPresignedBucketUrlRequest]):
        try:
            # Authorizer obrigatório
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if type(requester_user.user_id) != str:
                raise WrongTypeParameter(
                    field_name='user_id',
                    field_type_expected='str',
                    field_type_received=type(requester_user.user_id)
                )

            bucket = request.data.get("bucket")
            user_id = requester_user.user_id
            kb_id = request.data.get("kb_id")
            expires = request.data.get("expires", 900)
            max_size_mb = request.data.get("max_size_mb", 20)

            if not bucket:
                raise MissingParameters('bucket')

            if type(bucket) != str:
                raise WrongTypeParameter(
                    field_name="bucket",
                    field_type_expected="str",
                    field_type_received=bucket.__class__.__name__
                )

            if not user_id:
                raise MissingParameters('user_id')

            if type(user_id) != str:
                raise WrongTypeParameter(
                    field_name="user_id",
                    field_type_expected="str",
                    field_type_received=user_id.__class__.__name__
                )

            if not kb_id:
                raise MissingParameters('kb_id')

            if type(kb_id) != str:
                raise WrongTypeParameter(
                    field_name="kb_id",
                    field_type_expected="str",
                    field_type_received=kb_id.__class__.__name__
                )

            if not isinstance(expires, int):
                raise WrongTypeParameter(
                    field_name="expires",
                    field_type_expected="int",
                    field_type_received=expires.__class__.__name__
                )

            if not isinstance(max_size_mb, int):
                raise WrongTypeParameter(
                    field_name="max_size_mb",
                    field_type_expected="int",
                    field_type_received=max_size_mb.__class__.__name__
                )

            # Validar parâmetros na controller
            self._validate_parameters(bucket, user_id, kb_id, expires, max_size_mb)

            presigned_url = self.get_presigned_bucket_url_use_case(
                bucket.strip(), user_id.strip(), kb_id.strip(), expires, max_size_mb
            )

            return OK(body=presigned_url)

        except (MissingParameters, WrongTypeParameter) as err:
            return BadRequest(body={"error": "Parâmetros inválidos", "details": err.args[0]})

        except ValueError as err:
            return BadRequest(body={"error": "Dados inválidos", "details": str(err)})

        except ConfigurationError as err:
            return InternalServerError(body={"error": "Erro de configuração", "details": err.message})

        except ExternalServiceError as err:
            return InternalServerError(body={"error": "Erro de serviço", "details": err.message})

        except InfrastructureError as err:
            return InternalServerError(body={"error": "Erro de infraestrutura", "details": err.message})

        except Exception as err:
            return InternalServerError(body={"error": "Erro interno", "details": "Ocorreu um erro inesperado"})
