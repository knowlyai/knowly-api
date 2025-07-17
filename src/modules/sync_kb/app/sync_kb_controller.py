from src.modules.sync_kb.app.sync_kb_usecase import SyncKbUseCase
from src.modules.sync_kb.app.types import SyncKbRequest
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK


class SyncKbController:
    def __init__(self, sync_kb_usecase: SyncKbUseCase):
        self.sync_kb_usecase = sync_kb_usecase

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

            response = self.sync_kb_usecase(bucket_name, user_id, kb_id)
            return OK(body={"message": response})

        except WrongTypeParameter as err:
            return BadRequest(body=err.args[0])

        except MissingParameters as err:
            return BadRequest(body=err.args[0])

        except Exception as err:
            return InternalServerError(body=err.args[0])
