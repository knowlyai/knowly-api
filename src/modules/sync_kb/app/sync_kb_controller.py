from src.modules.sync_kb.app.sync_kb_usecase import SyncKbUseCase
from src.modules.sync_kb.app.types import SyncKbRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK, NotFound


class SyncKbController:
    def __init__(self, sync_kb_usecase: SyncKbUseCase):
        self.sync_kb_usecase = sync_kb_usecase

    def _validate_parameters(self, bucket_name: str, user_id: str, kb_id: str):
        """Valida os parâmetros de entrada na controller"""
        if not bucket_name or not bucket_name.strip():
            raise ValueError("Nome do bucket é obrigatório")

        if not user_id or not user_id.strip():
            raise ValueError("ID do usuário é obrigatório")

        if not kb_id or not kb_id.strip():
            raise ValueError("ID da base de conhecimento é obrigatório")

        if len(bucket_name.strip()) < 3:
            raise ValueError("Nome do bucket deve ter pelo menos 3 caracteres")

        if len(user_id.strip()) < 1:
            raise ValueError("ID do usuário não pode estar vazio")

        if len(kb_id.strip()) < 1:
            raise ValueError("ID da base de conhecimento não pode estar vazio")

    def __call__(self, request: IRequest[SyncKbRequest]):
        try:
            bucket_name = request.data.get("bucket_name")
            user_id = request.data.get("user_id")
            kb_id = request.data.get("kb_id")

            if not bucket_name:
                raise MissingParameters("bucket_name")

            if type(bucket_name) != str:
                raise WrongTypeParameter(
                    fieldName="bucket_name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=bucket_name.__class__.__name__
                )

            if not user_id:
                raise MissingParameters("user_id")

            if type(user_id) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=user_id.__class__.__name__
                )

            if not kb_id:
                raise MissingParameters("kb_id")

            if type(kb_id) != str:
                raise WrongTypeParameter(
                    fieldName="kb_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=kb_id.__class__.__name__
                )

            # Validar parâmetros na controller
            self._validate_parameters(bucket_name, user_id, kb_id)

            response = self.sync_kb_usecase(bucket_name.strip(), user_id.strip(), kb_id.strip())
            return OK(body={"message": response, "status": "Sincronização iniciada com sucesso"})

        except (MissingParameters, WrongTypeParameter) as err:
            return BadRequest(body={"error": "Parâmetros inválidos", "details": err.args[0]})

        except ValueError as err:
            return BadRequest(body={"error": "Dados inválidos", "details": str(err)})

        except NoItemsFound as err:
            return NotFound(body={"error": "Recurso não encontrado", "details": err.message})

        except ConfigurationError as err:
            return InternalServerError(body={"error": "Erro de configuração", "details": err.message})

        except ExternalServiceError as err:
            return InternalServerError(body={"error": "Erro de serviço", "details": err.message})

        except InfrastructureError as err:
            return InternalServerError(body={"error": "Erro de infraestrutura", "details": err.message})

        except Exception as err:
            return InternalServerError(body={"error": "Erro interno", "details": "Ocorreu um erro inesperado"})
