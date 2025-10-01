from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .sync_kb_controller import SyncKbController
from .sync_kb_usecase import SyncKbUseCase

use_case = SyncKbUseCase()
controller = SyncKbController(use_case)


def sync_kb_presenter(event):
    http_request = LambdaHttpRequest(event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()


def lambda_handler(event, context):
    response = sync_kb_presenter(event)
    return response
