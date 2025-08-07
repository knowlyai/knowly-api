from src.modules.get_kb.app.get_kb_controller import GetKbController
from src.modules.get_kb.app.get_kb_usecase import GetKbUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

use_case = GetKbUseCase()
controller = GetKbController(use_case)


def get_kb_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(response)
    return http_response.toDict()


def lambda_handler(event, context):
    response = get_kb_presenter(event)
    return response
