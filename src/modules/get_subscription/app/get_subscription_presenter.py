from .get_subscription_controller import GetSubscriptionController
from .get_subscription_usecase import GetSubscriptionUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from aws_lambda_powertools import Logger, Tracer, Metrics

observability = Environments.get_observability()(module_name="get_subscription")

repo = Environments.get_subscription_repo()()

usecase = GetSubscriptionUsecase(repo, observability=observability)
controller = GetSubscriptionController(usecase, observability=observability)


@observability.presenter_decorators
def get_subscription_presenter(event):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return httpResponse.toDict()


@observability.handler_decorators
def lambda_handler(event, context):
    response = get_subscription_presenter(event)

    if response.get("statusCode") != 200:
        observability.add_metric(name="ErrorCount", unit="Count", value=1)

    return response