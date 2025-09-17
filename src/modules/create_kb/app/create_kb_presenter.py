from .create_kb_controller import CreateKbController
from .create_kb_usecase import CreateKbUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()
use_case = CreateKbUseCase(repo=repo)
controller = CreateKbController(use_case)


def create_kb_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(response)
    return http_response.toDict()


def lambda_handler(event, context):
    response = create_kb_presenter(event)
    return response
