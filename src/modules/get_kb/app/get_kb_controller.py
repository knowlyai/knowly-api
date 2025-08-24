from src.modules.get_kb.app.get_kb_usecase import GetKbUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    DatabaseError,
    ConfigurationError
)
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK
from src.shared.infra.dto.user_api_gateway_dto import UserApiGatewayDTO


class GetKbController:
    def __init__(self, get_kb_usecase: GetKbUseCase):
        self.get_kb_usecase = get_kb_usecase

    def __call__(self, request: IRequest):
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

            # Extrair parâmetros
            user_id = requester_user.user_id
            kb_id = request.data.get("kb_id")

            # Validar kb_id se fornecido
            if kb_id is not None and type(kb_id) != str:
                raise WrongTypeParameter(
                    fieldName="kb_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=kb_id.__class__.__name__
                )

            # Executar use case
            result = self.get_kb_usecase.get_knowledge_bases(user_id, kb_id)

            return OK(body=result)

        except MissingParameters as e:
            return BadRequest(body=e.message)

        except WrongTypeParameter as e:
            return BadRequest(body=e.message)

        except ValueError as e:
            return BadRequest(body={"error": "Parâmetros inválidos", "details": str(e)})

        except DatabaseError as e:
            return InternalServerError(body={"error": "Erro de banco de dados", "details": str(e)})

        except ConfigurationError as e:
            return InternalServerError(body={"error": "Erro de configuração", "details": str(e)})

        except ExternalServiceError as e:
            return InternalServerError(body={"error": "Erro de serviço externo", "details": str(e)})

        except InfrastructureError as e:
            return InternalServerError(body={"error": "Erro de infraestrutura", "details": str(e)})

        except Exception as e:
            return InternalServerError(body={"error": "Erro interno", "details": "Ocorreu um erro inesperado"})
