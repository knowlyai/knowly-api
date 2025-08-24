from src.modules.delete_kb_file.app.delete_kb_file_controller import DeleteKbFileController
from src.modules.delete_kb_file.app.delete_kb_file_usecase import DeleteKbFileUseCase
from src.shared.helpers.external_interfaces.http_lambda_requests import LambdaHttpRequest, LambdaHttpResponse

use_case = DeleteKbFileUseCase()
controller = DeleteKbFileController(use_case)

def delete_kb_file_presenter(event):
    http_request = LambdaHttpRequest(event)
    response = controller(http_request)
    http_response = LambdaHttpResponse(response)
    return http_response.toDict()

def lambda_handler(event, context):
    response = delete_kb_file_presenter(event)
    return response

