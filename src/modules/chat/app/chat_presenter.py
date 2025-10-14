from .chat_controller import ChatController
from .chat_usecase import ChatUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse
from src.shared.infra.repositories.keys_repository_dynamo import KeysRepositoryDynamo

keys_repo = KeysRepositoryDynamo()
use_case = ChatUseCase(keys_repository=keys_repo)
controller = ChatController(use_case)

def chat_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(status_code=response.status_code, body=response.body, headers=response.headers)
    return http_response.toDict()

def lambda_handler(event, context):
    response = chat_presenter(event)
    return response
