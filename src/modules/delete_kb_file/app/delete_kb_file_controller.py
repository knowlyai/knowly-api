from src.modules.delete_kb_file.app.delete_kb_file_usecase import DeleteKbFileUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK, NotFound


class DeleteKbFileController:
    def __init__(self, delete_kb_file_usecase: DeleteKbFileUseCase):
        self.delete_kb_file_usecase = delete_kb_file_usecase

    def _validate_parameters(self, bucket: str, user_id: str, kb_id: str, file_name: str):
        """Valida os parâmetros de entrada na controller"""
        if not bucket or not bucket.strip():
            raise ValueError("Nome do bucket é obrigatório")

        if not user_id or not user_id.strip():
            raise ValueError("ID do usuário é obrigatório")

        if not kb_id or not kb_id.strip():
            raise ValueError("ID da base de conhecimento é obrigatório")

        if not file_name or not file_name.strip():
            raise ValueError("Nome do arquivo é obrigatório")

        if len(bucket.strip()) < 3:
            raise ValueError("Nome do bucket deve ter pelo menos 3 caracteres")

        if len(user_id.strip()) < 1:
            raise ValueError("ID do usuário não pode estar vazio")

        if len(kb_id.strip()) < 1:
            raise ValueError("ID da base de conhecimento não pode estar vazio")

        if len(file_name.strip()) < 1:
            raise ValueError("Nome do arquivo não pode estar vazio")

    def __call__(self, request: IRequest):
        try:
            bucket = request.data.get("bucket")
            user_id = request.data.get("user_id")
            kb_id = request.data.get("kb_id")
            file_name = request.data.get("file_name")

            if not bucket:
                raise MissingParameters('bucket')
            if type(bucket) != str:
                raise WrongTypeParameter(
                    fieldName="bucket",
                    fieldTypeExpected="str",
                    fieldTypeReceived=bucket.__class__.__name__
                )
            if not user_id:
                raise MissingParameters('user_id')
            if type(user_id) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=user_id.__class__.__name__
                )
            if not kb_id:
                raise MissingParameters('kb_id')
            if type(kb_id) != str:
                raise WrongTypeParameter(
                    fieldName="kb_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=kb_id.__class__.__name__
                )
            if not file_name:
                raise MissingParameters('file_name')
            if type(file_name) != str:
                raise WrongTypeParameter(
                    fieldName="file_name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=file_name.__class__.__name__
                )

            # Validar parâmetros na controller
            self._validate_parameters(bucket, user_id, kb_id, file_name)

            result = self.delete_kb_file_usecase(
                bucket.strip(), user_id.strip(), kb_id.strip(), file_name.strip()
            )
            return OK(body={"message": result, "status": "Arquivo deletado com sucesso"})

        except (MissingParameters, WrongTypeParameter) as err:
            return BadRequest(body={"error": "Parâmetros inválidos", "details": err.args[0]})

        except ValueError as err:
            return BadRequest(body={"error": "Dados inválidos", "details": str(err)})

        except NoItemsFound as err:
            return NotFound(body={"error": "Arquivo não encontrado", "details": err.message})

        except ConfigurationError as err:
            return InternalServerError(body={"error": "Erro de configuração", "details": err.message})

        except ExternalServiceError as err:
            return InternalServerError(body={"error": "Erro de serviço", "details": err.message})

        except InfrastructureError as err:
            return InternalServerError(body={"error": "Erro de infraestrutura", "details": err.message})

        except Exception as err:
            return InternalServerError(body={"error": "Erro interno", "details": "Ocorreu um erro inesperado"})
