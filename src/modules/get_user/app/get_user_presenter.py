from .get_user_controller import GetUserController
from .get_user_usecase import GetUserUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_user_repo()
use_case = GetUserUseCase(repo)
controller = GetUserController(use_case)


def get_user_presenter(event):
    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()


def lambda_handler(event, context):
    response = get_user_presenter(event)
    return response
