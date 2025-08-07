from src.modules.chat.app.chat_usecase import ChatUseCase
from src.shared.domain.enums.models_enum import Models
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import (
    ExternalServiceError,
    InfrastructureError,
    ConfigurationError,
    NoItemsFound
)
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK, NotFound

class ChatController:
    def __init__(self, chat_usecase: ChatUseCase):
        self.chat_usecase = chat_usecase

    def _validate_parameters(self, kb_id: str, prompt: str, top_k: int):
        """Valida os parâmetros de entrada na controller"""
        if not kb_id or not kb_id.strip():
            raise ValueError("ID da base de conhecimento é obrigatório")

        if not prompt or not prompt.strip():
            raise ValueError("Prompt é obrigatório")

        if len(kb_id.strip()) < 1:
            raise ValueError("ID da base de conhecimento não pode estar vazio")

        if len(prompt.strip()) < 1:
            raise ValueError("Prompt não pode estar vazio")

    def __call__(self, request: IRequest):
        try:
            kb_id = request.data.get("kb_id")
            model = request.data.get("model")
            prompt = request.data.get("prompt")
            top_k = request.data.get("top_k", 5)

            if not kb_id:
                raise MissingParameters('kb_id')
            if type(kb_id) != str:
                raise WrongTypeParameter(
                    fieldName="kb_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=kb_id.__class__.__name__
                )
            if not model:
                raise MissingParameters('model')
            if type(model) != Models:
                raise WrongTypeParameter(
                    fieldName="model",
                    fieldTypeExpected="Models",
                    fieldTypeReceived=model.__class__.__name__
                )
            if not prompt:
                raise MissingParameters('prompt')
            if type(prompt) != str:
                raise WrongTypeParameter(
                    fieldName="prompt",
                    fieldTypeExpected="str",
                    fieldTypeReceived=prompt.__class__.__name__
                )
            if type(top_k) != int:
                raise WrongTypeParameter(
                    fieldName="top_k",
                    fieldTypeExpected="int",
                    fieldTypeReceived=top_k.__class__.__name__
                )

            # Validar parâmetros na controller
            self._validate_parameters(kb_id, prompt, top_k)

            result = self.chat_usecase(
                kb_id=kb_id.strip(),
                model=model.value,
                prompt=prompt.strip(),
                top_k=top_k
            )
            return OK(body={
                result
            })

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
