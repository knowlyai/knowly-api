from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_controller import GetPresignedBucketUrlController
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

use_case = GetPresignedBucketUrlUseCase()
controller = GetPresignedBucketUrlController(use_case)


def get_user_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(response)
    return http_response.toDict()


def lambda_handler(event, context):
    response = get_user_presenter(event)
    return response
