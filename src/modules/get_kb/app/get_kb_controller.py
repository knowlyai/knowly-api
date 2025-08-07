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


class GetKbController:
    def __init__(self, get_kb_usecase: GetKbUseCase):
        self.get_kb_usecase = get_kb_usecase

    def __call__(self, request: IRequest):
        try:
            # Extrair parâmetros
            user_id = request.data.get("user_id")
            kb_id = request.data.get("kb_id")

            # Validar parâmetros obrigatórios
            if not user_id:
                raise MissingParameters('user_id')

            if type(user_id) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=user_id.__class__.__name__
                )

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
