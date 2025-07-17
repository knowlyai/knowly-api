from src.modules.delete_kb_file.app.delete_kb_file_usecase import DeleteKbFileUseCase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, BadRequest, OK


class DeleteKbFileController:
    def __init__(self, delete_kb_file_usecase: DeleteKbFileUseCase):
        self.delete_kb_file_usecase = delete_kb_file_usecase

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

            result = self.delete_kb_file_usecase(bucket, user_id, kb_id, file_name)
            return OK(body={"message": result})

        except WrongTypeParameter as err:
            return BadRequest(body=err.args[0])

        except MissingParameters as err:
            return BadRequest(body=err.args[0])

        except Exception as err:
            return InternalServerError(body=err.args[0])
