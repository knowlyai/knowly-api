from fastapi import APIRouter, HTTPException
from src.modules.get_user.app.get_user_controller import GetUserController
from src.modules.get_user.app.get_user_usecase import GetUserUseCase
from src.shared.environments import Environments
from src.shared.helpers.external_interfaces.external_interface import IRequest
from src.shared.helpers.external_interfaces.http_models import HttpRequest

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{user_id}", summary="Obter um usuário")
async def get_user(user_id: str):
    repo = Environments.get_user_repo()
    use_case = GetUserUseCase(repo)
    controller = GetUserController(use_case)
    request = HttpRequest({
        'user_id': user_id
    })
    user = controller(request)

    if not user:
        raise HTTPException(
            status_code=404, detail="Usuário não encontrado"
        )

    return user.data
