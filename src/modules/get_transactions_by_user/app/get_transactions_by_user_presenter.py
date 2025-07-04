from .get_transactions_by_user_controller import GetTransactionsByUserController
from .get_transactions_by_user_usecase import GetTransactionsByUserUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo = Environments.get_transaction_repo()()
usecase = GetTransactionsByUserUseCase(repo=repo)
controller = GetTransactionsByUserController(usecase=usecase)

def lambda_handler(event, context):
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(request=httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )
    return httpResponse.toDict()