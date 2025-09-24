from .get_kb_controller import GetKbController
from .get_kb_usecase import GetKbUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse


repo = Environments.get_user_repo()
use_case = GetKbUseCase(repo=repo)
controller = GetKbController(use_case)


def get_kb_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()


def lambda_handler(event, context):
    response = get_kb_presenter(event)
    return response
