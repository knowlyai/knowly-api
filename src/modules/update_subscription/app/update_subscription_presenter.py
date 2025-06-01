from .update_subscription_controller import UpdateSubscriptionController
from .update_subscription_usecase import UpdateSubscriptionUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_subscription_repo()()
usecase = UpdateSubscriptionUsecase(repo)
controller = UpdateSubscriptionController(usecase)


def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )

    return httpResponse.toDict()