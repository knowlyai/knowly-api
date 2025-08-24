from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

from src.modules.get_token.app.get_token_controller import GetTokenController
from src.modules.get_token.app.get_token_usecase import GetTokenUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest, HttpResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/token", summary="Obtém tokens de autenticação (Cognito)")
async def get_token(body: AuthRequest):
    try:
        use_case = GetTokenUseCase()
        controller = GetTokenController(use_case)
        body_dict = {"email": body.email, "password": body.password}
        request = HttpRequest(body=body_dict)
        response: HttpResponse = controller(request)  # type: ignore[assignment]

        return JSONResponse(status_code=response.status_code, content=response.body)

    except Exception:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao autenticar"
            }
        )
