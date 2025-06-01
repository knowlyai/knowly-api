from .get_transactions_by_user_controller import GetTransactionsByUserController
from .get_transactions_by_user_usecase import GetTransactionsByUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS

# Inicializa o componente de observabilidade para este módulo
observability = Environments.get_observability()(module_name="get_transactions_by_user")

# Instancia o repositório e o use case
repo = Environments.get_transaction_repo()()
usecase = GetTransactionsByUserUsecase(repo=repo, observability=observability)
controller = GetTransactionsByUserController(usecase=usecase, observability=observability)


@observability.presenter_decorators
def get_transactions_by_user_presenter(event):
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
    response = get_transactions_by_user_presenter(event)
    if response.get("statusCode") != 200:
        observability.add_metric(name="ErrorCount", unit="Count", value=1)
    return response