from src.modules.create_kb.app.create_kb_usecase import CreateKbUseCase
from src.modules.create_kb.app.types import CreateKbRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, Created


class CreateKbController:
    def __init__(self, create_kb_usecase: CreateKbUseCase):
        self.create_kb_usecase = create_kb_usecase

    def __call__(self, request: IRequest[CreateKbRequest]):
        try:
            kb_name = request.data.get("kb_name")
            kb_description = request.data.get("kb_description")

            if not kb_name:
                raise MissingParameters('kb_name')

            if type(kb_name) != str:
                raise WrongTypeParameter(
                    fieldName="kb_name",
                    fieldTypeExpected="str",
                    fieldTypeReceived=kb_name.__class__.__name__
                )

            if not kb_description:
                raise MissingParameters('kb_description')

            if type(kb_description) != str:
                raise WrongTypeParameter(
                    fieldName="kb_description",
                    fieldTypeExpected="str",
                    fieldTypeReceived=kb_description.__class__.__name__
                )

            kb_id = self.create_kb_usecase(kb_name, kb_description)
            return Created(body={"kb_id": kb_id})

        except WrongTypeParameter as err:
            return BadRequest(body=err.args[0])

        except MissingParameters as err:
            return BadRequest(body=err.args[0])

        except Exception as err:
            return InternalServerError(body=err.args[0])
