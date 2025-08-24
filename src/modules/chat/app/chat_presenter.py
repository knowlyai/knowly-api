from src.modules.chat.app.chat_controller import ChatController
from src.modules.chat.app.chat_usecase import ChatUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

use_case = ChatUseCase()
controller = ChatController(use_case)

def chat_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(response)
    return http_response.toDict()

def lambda_handler(event, context):
    response = chat_presenter(event)
    return response
