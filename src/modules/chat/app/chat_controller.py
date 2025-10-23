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
from .chat_usecase import ChatUseCase


class ChatController:
    def __init__(self, chat_usecase: ChatUseCase):
        self.chat_usecase = chat_usecase

    def _validate_parameters(self, kb_key: str, prompt: str, top_k: int):
        """Valida os parâmetros de entrada na controller"""
        if not kb_key or not kb_key.strip():
            raise ValueError("kb_key é obrigatória")

        if not prompt or not prompt.strip():
            raise ValueError("Prompt é obrigatório")

        if len(kb_key.strip()) < 1:
            raise ValueError("kb_key não pode estar vazia")

        if len(prompt.strip()) < 1:
            raise ValueError("Prompt não pode estar vazio")

    def __call__(self, request: IRequest):
        try:
            kb_key = request.data.get("kb_key")
            model = request.data.get("model")
            prompt = request.data.get("prompt")
            top_k = request.data.get("top_k", 5)

            if not kb_key:
                raise MissingParameters('kb_key')
            if type(kb_key) != str:
                raise WrongTypeParameter(
                    field_name="kb_key",
                    field_type_expected="str",
                    field_type_received=kb_key.__class__.__name__
                )
            if not model:
                raise MissingParameters('model')

            # Converter string para enum Models
            if type(model) == str:
                try:
                    model = Models[model]
                except KeyError:
                    raise ValueError(f"Modelo '{model}' não é válido. Modelos disponíveis: {', '.join([m.name for m in Models])}")

            if type(model) != Models:
                raise WrongTypeParameter(
                    field_name="model",
                    field_type_expected="Models",
                    field_type_received=model.__class__.__name__
                )
            if not prompt:
                raise MissingParameters('prompt')
            if type(prompt) != str:
                raise WrongTypeParameter(
                    field_name="prompt",
                    field_type_expected="str",
                    field_type_received=prompt.__class__.__name__
                )
            if type(top_k) != int:
                raise WrongTypeParameter(
                    field_name="top_k",
                    field_type_expected="int",
                    field_type_received=top_k.__class__.__name__
                )

            # Validar parâmetros na controller
            self._validate_parameters(kb_key, prompt, top_k)

            result = self.chat_usecase(
                kb_key=kb_key.strip(),
                model=model.value,
                prompt=prompt.strip(),
                top_k=top_k
            )
            return OK(body={
                'answer': result['answer']
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
