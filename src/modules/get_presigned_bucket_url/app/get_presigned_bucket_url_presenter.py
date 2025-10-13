from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_presigned_bucket_url_controller import GetPresignedBucketUrlController
from .get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase

repo = Environments.get_user_repo()
use_case = GetPresignedBucketUrlUseCase(repo=repo)
controller = GetPresignedBucketUrlController(use_case)


def get_presigned_bucket_url_presenter(event):
    http_request = LambdaHttpRequest(event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()


def lambda_handler(event, context):
    response = get_presigned_bucket_url_presenter(event)
    return response
