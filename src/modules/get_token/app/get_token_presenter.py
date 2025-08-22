from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.helpers.external_interfaces.http_models import HttpResponse
from .get_token_controller import GetTokenController
from .get_token_usecase import GetTokenUseCase

usecase = GetTokenUseCase()
controller = GetTokenController(usecase)


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    response: HttpResponse = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()
