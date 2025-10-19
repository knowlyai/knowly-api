from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import (
    DuplicatedItem,
    ExternalServiceError,
    InfrastructureError,
    DatabaseError,
    ConfigurationError,
    PlanQuotaExceeded
)
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, Created, Conflict, Forbidden
from src.shared.infra.dto.user_api_gateway_dto import UserApiGatewayDTO
from .create_kb_usecase import CreateKbUseCase
from .types import CreateKbRequest


class CreateKbController:
    def __init__(self, create_kb_usecase: CreateKbUseCase):
        self.create_kb_usecase = create_kb_usecase

    def _validate_parameters(self, kb_name: str, kb_description: str, kb_display_name: str):
        """Valida os parâmetros de entrada"""
        if not kb_name or not kb_name.strip():
            raise ValueError("Nome da base de conhecimento é obrigatório")

        if not kb_description or not kb_description.strip():
            raise ValueError("Descrição da base de conhecimento é obrigatória")

        if not kb_display_name or not kb_display_name.strip():
            raise ValueError("Nome de exibição da base de conhecimento é obrigatório")

        if len(kb_name.strip()) < 3:
            raise ValueError("Nome da base de conhecimento deve ter pelo menos 3 caracteres")

        if len(kb_name.strip()) > 100:
            raise ValueError("Nome da base de conhecimento deve ter no máximo 100 caracteres")

        if len(kb_display_name.strip()) < 3:
            raise ValueError("Nome de exibição deve ter pelo menos 3 caracteres")

        if len(kb_display_name.strip()) > 100:
            raise ValueError("Nome de exibição deve ter no máximo 100 caracteres")

        if len(kb_description.strip()) > 500:
            raise ValueError("Descrição da base de conhecimento deve ter no máximo 500 caracteres")

    def __call__(self, request: IRequest[CreateKbRequest]):
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

            kb_name = request.data.get("kb_name")
            kb_description = request.data.get("kb_description")
            kb_display_name = request.data.get("kb_display_name")

            if not kb_name:
                raise MissingParameters('kb_name')

            if type(kb_name) != str:
                raise WrongTypeParameter(
                    field_name="kb_name",
                    field_type_expected="str",
                    field_type_received=kb_name.__class__.__name__
                )

            if not kb_description:
                raise MissingParameters('kb_description')

            if type(kb_description) != str:
                raise WrongTypeParameter(
                    field_name="kb_description",
                    field_type_expected="str",
                    field_type_received=kb_description.__class__.__name__
                )

            if not kb_display_name:
                raise MissingParameters('kb_display_name')

            if type(kb_display_name) != str:
                raise WrongTypeParameter(
                    field_name="kb_display_name",
                    field_type_expected="str",
                    field_type_received=kb_display_name.__class__.__name__
                )

            # Validar parâmetros na controller
            self._validate_parameters(kb_name, kb_description, kb_display_name)

            kb_id, kb_key = self.create_kb_usecase(kb_name.strip(), kb_description.strip(), kb_display_name.strip(), requester_user.user_id)
            return Created(body={
                "kb_id": kb_id,
                "kb_key": kb_key,
                "details": "Base de conhecimento criada com sucesso"
            })

        except (MissingParameters, WrongTypeParameter) as err:
            return BadRequest(body={"error": "Parâmetros inválidos", "details": err.args[0]})

        except ValueError as err:
            return BadRequest(body={"error": "Dados inválidos", "details": str(err)})

        except PlanQuotaExceeded as err:
            return Forbidden(body={"error": "Limite do plano excedido", "details": err.message})

        except DuplicatedItem as err:
            return Conflict(body={"error": "Recurso já existe", "details": err.message})

        except ConfigurationError as err:
            return InternalServerError(body={"error": "Erro de configuração", "details": err.message})

        except (ExternalServiceError, DatabaseError) as err:
            return InternalServerError(body={"error": "Erro de serviço", "details": err.message})

        except InfrastructureError as err:
            return InternalServerError(body={"error": "Erro de infraestrutura", "details": err.message})

        except Exception as err:
            return InternalServerError(body={"error": "Erro interno", "details": "Ocorreu um erro inesperado"})
