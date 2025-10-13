from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Annotated
import jwt

from src.modules.create_kb.app.create_kb_controller import CreateKbController
from src.modules.get_kb.app.get_kb_controller import GetKbController
from src.modules.get_kb.app.get_kb_usecase import GetKbUseCase
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_controller import GetPresignedBucketUrlController
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase
from src.modules.create_kb.app.create_kb_usecase import CreateKbUseCase
from src.modules.sync_kb.app.sync_kb_controller import SyncKbController
from src.modules.sync_kb.app.sync_kb_usecase import SyncKbUseCase
from src.modules.delete_kb_file.app.delete_kb_file_controller import DeleteKbFileController
from src.modules.delete_kb_file.app.delete_kb_file_usecase import DeleteKbFileUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from pydantic import BaseModel
from src.shared.infra.repositories.user_repository_dynamo import UserRepositoryDynamo

router = APIRouter(prefix="/kb", tags=["Knowledge Bases"])

security = HTTPBearer()

class CreateKbRequest(BaseModel):
    kb_name: str
    kb_description: str
    kb_display_name: str

@router.post("", summary="Cria uma base de conhecimento na AWS")
async def create_kb(body: CreateKbRequest, token: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        use_case = CreateKbUseCase()
        controller = CreateKbController(use_case)
        body_dict = {
            "kb_name": body.kb_name,
            "kb_description": body.kb_description,
            "kb_display_name": body.kb_display_name
        }
        try:
            claims = jwt.decode(token.credentials, options={"verify_signature": False}, algorithms=["RS256"])  # validação simplificada
            sub = claims.get("sub")
            body_dict['requester_user'] = { "sub": sub, "name": "", "email": "" }
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
        request = HttpRequest(body=body_dict)
        response = controller(request)

        # Retornar resposta com o código HTTP correto
        return JSONResponse(
            status_code=response.status_code,
            content=response.body
        )

    except HTTPException:
        raise
    except Exception as e:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao criar a base de conhecimento"
            }
        )


@router.get("/presigned-url", summary="Gera URL Presigned para enviar arquivos para uma base de conhecimento")
async def get_url_presigned(bucket: str, kb_id: str, expires: int = 900, max_size_mb: int = 20, token: Annotated[HTTPAuthorizationCredentials, Depends(security)] = None):
    try:
        use_case = GetPresignedBucketUrlUseCase()
        controller = GetPresignedBucketUrlController(use_case)
        params = {
            "bucket": bucket,
            "kb_id": kb_id,
            "expires": expires,
            "max_size_mb": max_size_mb
        }
        try:
            claims = jwt.decode(token.credentials, options={"verify_signature": False}, algorithms=["RS256"])  # validação simplificada
            sub = claims.get("sub")
            params['requester_user'] = {"sub": sub, "name": "", "email": ""}
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
        request = HttpRequest(query_params=params)
        response = controller(request)

        # Retornar resposta com o código HTTP correto
        return JSONResponse(
            status_code=response.status_code,
            content=response.body
        )

    except HTTPException:
        raise
    except Exception as e:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao gerar URL pré-assinada"
            }
        )


@router.get("/sync", summary="Sincroniza uma base de conhecimento com os arquivos enviados para o S3")
async def sync_kb(bucket_name: str, kb_id: str, token: Annotated[HTTPAuthorizationCredentials, Depends(security)] = None):
    try:
        use_case = SyncKbUseCase()
        controller = SyncKbController(use_case)
        params = {
            "bucket_name": bucket_name,
            "kb_id": kb_id
        }
        try:
            claims = jwt.decode(token.credentials, options={"verify_signature": False}, algorithms=["RS256"])  # validação simplificada
            sub = claims.get("sub")
            params['requester_user'] = {"sub": sub, "name": "", "email": ""}
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
        request = HttpRequest(query_params=params)
        response = controller(request)

        # Retornar resposta com o código HTTP correto
        return JSONResponse(
            status_code=response.status_code,
            content=response.body
        )

    except HTTPException:
        raise
    except Exception as e:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao sincronizar a base de conhecimento"
            }
        )


@router.delete("/file", summary="Deleta um arquivo de uma base de conhecimento no S3")
async def delete_kb_file(bucket: str, kb_id: str, file_name: str, token: Annotated[HTTPAuthorizationCredentials, Depends(security)] = None):
    try:
        use_case = DeleteKbFileUseCase()
        controller = DeleteKbFileController(use_case)
        params = {
            "bucket": bucket,
            "kb_id": kb_id,
            "file_name": file_name
        }
        try:
            claims = jwt.decode(token.credentials, options={"verify_signature": False}, algorithms=["RS256"])  # validação simplificada
            sub = claims.get("sub")
            params['requester_user'] = {"sub": sub, "name": "", "email": ""}
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
        request = HttpRequest(query_params=params)
        response = controller(request)

        # Retornar resposta com o código HTTP correto
        return JSONResponse(
            status_code=response.status_code,
            content=response.body
        )

    except HTTPException:
        raise
    except Exception as e:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao deletar arquivo da base de conhecimento"
            }
        )


@router.get("", summary="Lista as bases de conhecimento")
async def list_kbs(kb_id: Optional[str] = Query(None, description="ID da base de conhecimento"), token: Annotated[HTTPAuthorizationCredentials, Depends(security)] = None):
    try:
        use_case = GetKbUseCase(repo=UserRepositoryDynamo())
        controller = GetKbController(use_case)
        params = {
            "kb_id": kb_id
        }
        try:
            claims = jwt.decode(token.credentials, options={"verify_signature": False}, algorithms=["RS256"])  # validação simplificada
            sub = claims.get("sub")
            params["requester_user"] = {"sub": sub, "name": "", "email": ""}
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido")
        request = HttpRequest(query_params=params)
        response = controller(request)

        # Retornar resposta com o código HTTP correto
        return JSONResponse(
            status_code=response.status_code,
            content=response.body
        )

    except HTTPException:
        raise
    except Exception as e:
        # Fallback para erros não tratados pela controller interna
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno",
                "details": "Ocorreu um erro inesperado ao listar as bases de conhecimento"
            }
        )
