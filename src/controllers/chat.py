from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.modules.chat.app.chat_controller import ChatController
from src.modules.chat.app.chat_usecase import ChatUseCase
from src.shared.domain.enums.models_enum import Models
from src.shared.helpers.external_interfaces.http_models import HttpRequest

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    kb_id: str
    model: Models
    prompt: str
    top_k: int = 5

@router.post("", summary="Envia uma mensagem para o chat e recebe uma resposta + citações")
async def chat(body: ChatRequest):
    try:
        use_case = ChatUseCase()
        controller = ChatController(use_case)
        body_dict = {
            "kb_id": body.kb_id,
            "model": body.model,
            "prompt": body.prompt,
            "top_k": body.top_k
        }
        request = HttpRequest(body=body_dict)
        response = controller(request)

        # Retornar resposta com o código HTTP correto
        return JSONResponse(
            status_code=response.status_code,
            content=response.body
        )

    except Exception as e:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao processar mensagem do chat"
            }
        )
