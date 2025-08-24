from src.modules.sync_kb.app.sync_kb_controller import SyncKbController
from src.modules.sync_kb.app.sync_kb_usecase import SyncKbUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

use_case = SyncKbUseCase()
controller = SyncKbController(use_case)


def sync_kb_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(response)
    return http_response.toDict()


def lambda_handler(event, context):
    response = sync_kb_presenter(event)
    return response
