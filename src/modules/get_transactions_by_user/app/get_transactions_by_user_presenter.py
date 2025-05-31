from .get_transactions_by_user_controller import GetTransactionsByUserController
from .get_transactions_by_user_usecase import GetTransactionsByUserUsecase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

repo_transaction = Environments.get_transaction_repo()()
usecase = GetTransactionsByUserUsecase(repo_transaction)
controller = GetTransactionsByUserController(usecase=usecase)


def lambda_handler(event, context):
    
    httpRequest = LambdaHttpRequest(data=event)
    response = controller(httpRequest)
    httpResponse = LambdaHttpResponse(
        status_code=response.status_code,
        body=response.body,
        headers=response.headers
    )

    return httpResponse.toDict()