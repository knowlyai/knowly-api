from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase
from src.modules.get_presigned_bucket_url.app.types import GetPresignedBucketUrlRequest
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter


class GetPresignedBucketUrlController:
    def __init__(self, get_presigned_bucket_url_use_case: GetPresignedBucketUrlUseCase):
        self.get_presigned_bucket_url_use_case = get_presigned_bucket_url_use_case

    def __call__(self, request: IRequest[GetPresignedBucketUrlRequest]):
        try:
            bucket = request.data.get("bucket")
            user_id = request.data.get("user_id")
            kb_id = request.data.get("kb_id")
            expires = request.data.get("expires", 900)
            max_size_mb = request.data.get("max_size_mb", 20)

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

            if not isinstance(expires, int):
                raise WrongTypeParameter(
                    fieldName="expires",
                    fieldTypeExpected="int",
                    fieldTypeReceived=expires.__class__.__name__
                )

            if not isinstance(max_size_mb, int):
                raise WrongTypeParameter(
                    fieldName="max_size_mb",
                    fieldTypeExpected="int",
                    fieldTypeReceived=max_size_mb.__class__.__name__
                )

            presigned_url = self.get_presigned_bucket_url_use_case(bucket, user_id, kb_id, expires, max_size_mb)
            response = OK(presigned_url)
            return response
        except Exception as err:
            return InternalServerError(body=err.args[0])
