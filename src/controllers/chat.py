from fastapi import APIRouter, HTTPException

from src.modules.chat.app.chat_controller import ChatController
from src.modules.chat.app.chat_usecase import ChatUseCase
from src.shared.domain.enums.models_enum import Models
from src.shared.helpers.external_interfaces.http_models import HttpRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", summary="Envia uma mensagem para o chat e recebe uma resposta + citações")
async def chat(kb_id: str, model: Models, prompt: str, top_k: int = 5):
    use_case = ChatUseCase()
    controller = ChatController(use_case)
    params = {
        "kb_id": kb_id,
        "model": model,
        "prompt": prompt,
        "top_k": top_k
    }
    request = HttpRequest(query_params=params)
    response = controller(request)

    if not response:
        raise HTTPException(
            status_code=500, detail="Algo deu errado ao processar a mensagem do chat"
        )

    return response.data
