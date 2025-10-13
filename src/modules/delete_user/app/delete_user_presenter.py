from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from .delete_user_controller import DeleteUserController
from .delete_user_usecase import DeleteUserUseCase

repo = Environments.get_user_repo()
usecase = DeleteUserUseCase(repo)
controller = DeleteUserController(usecase)


def lambda_handler(event, context):
    http_request = LambdaHttpRequest(data=event)
    # Injeta o usuário autenticado vindo do API Gateway/Cognito para o controller
    http_request.data['requester_user'] = event.get('requestContext', {}).get('authorizer', {}).get('claims', None)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)

    return http_response.toDict()
