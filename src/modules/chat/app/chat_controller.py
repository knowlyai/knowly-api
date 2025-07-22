from src.modules.chat.app.chat_usecase import ChatUseCase
from src.shared.domain.enums.models_enum import Models
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK

class ChatController:
    def __init__(self, chat_usecase: ChatUseCase):
        self.chat_usecase = chat_usecase

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
                    fieldTypeExpected="str",
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

            result = self.chat_usecase(kb_id=kb_id, model=model.value, prompt=prompt, top_k=top_k)
            return OK(body=result)

        except WrongTypeParameter as err:
            return BadRequest(body=err.args[0])
        except MissingParameters as err:
            return BadRequest(body=err.args[0])
        except Exception as err:
            return InternalServerError(body=err.args[0])
