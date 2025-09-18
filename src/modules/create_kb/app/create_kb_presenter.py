from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .create_kb_controller import CreateKbController
from .create_kb_usecase import CreateKbUseCase

repo = Environments.get_user_repo()
use_case = CreateKbUseCase(repo=repo)
controller = CreateKbController(use_case)


def create_kb_presenter(event):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()


def lambda_handler(event, context):
    response = create_kb_presenter(event)
    return response
