from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .get_subscriptions_by_user_controller import GetUserSubscriptionsController
from .get_subscriptions_by_user_usecase import GetUserSubscriptionsUseCase

repo = Environments.get_user_repo()()
usecase = GetUserSubscriptionsUseCase(repo=repo)
controller = GetUserSubscriptionsController(usecase=usecase)

def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)

    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )

    return http_response.toDict()