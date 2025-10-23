from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .delete_kb_file_controller import DeleteKbFileController
from .delete_kb_file_usecase import DeleteKbFileUseCase

use_case = DeleteKbFileUseCase()
controller = DeleteKbFileController(use_case)

def delete_kb_file_presenter(event):
    http_request = LambdaHttpRequest(event)
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()

def lambda_handler(event, context):
    response = delete_kb_file_presenter(event)
    return response

