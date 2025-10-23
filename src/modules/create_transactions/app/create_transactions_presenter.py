from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .create_transactions_controller import CreateTransactionController
from .create_transactions_usecase import CreateTransactionUsecase

def lambda_handler(event, context):
    repo = Environments.get_user_repo()  
    usecase = CreateTransactionUsecase(repo)
    controller = CreateTransactionController(usecase)

    http_request = LambdaHttpRequest(data=event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return http_response.toDict()