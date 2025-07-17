from fastapi import APIRouter, HTTPException

from src.modules.create_kb.app.create_kb_controller import CreateKbController
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_controller import GetPresignedBucketUrlController
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase
from src.modules.create_kb.app.create_kb_usecase import CreateKbUseCase
from src.modules.sync_kb.app.sync_kb_controller import SyncKbController
from src.modules.sync_kb.app.sync_kb_usecase import SyncKbUseCase
from src.modules.delete_kb_file.app.delete_kb_file_controller import DeleteKbFileController
from src.modules.delete_kb_file.app.delete_kb_file_usecase import DeleteKbFileUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest

router = APIRouter(prefix="/kb", tags=["Knowledge Bases"])


@router.post("", summary="Cria uma base de conhecimento na AWS")
async def create_kb(kb_name: str, kb_description: str):
    use_case = CreateKbUseCase()
    controller = CreateKbController(use_case)
    params = {
        "kb_name": kb_name,
        "kb_description": kb_description
    }
    request = HttpRequest(query_params=params)
    response = controller(request)

    if not response:
        raise HTTPException(
            status_code=500, detail="Algo deu errado ao criar a base de conhecimento"
        )

    return response.data


@router.get("/url-presigned", summary="Gera URL Presigned para enviar arquivos para uma base de conhecimento")
async def get_url_presigned(bucket: str, user_id: str, kb_id: str, expires: int = 900, max_size_mb: int = 20):
    use_case = GetPresignedBucketUrlUseCase()
    controller = GetPresignedBucketUrlController(use_case)
    params = {
        "bucket": bucket,
        "user_id": user_id,
        "kb_id": kb_id,
        "expires": expires,
        "max_size_mb": max_size_mb
    }
    request = HttpRequest(query_params=params)
    response = controller(request)

    if not response:
        raise HTTPException(
            status_code=500, detail="Algo deu errado ao gerar URL pré-assinada"
        )

    return response.data


@router.get("/sync", summary="Sincroniza uma base de conhecimento com os arquivos enviados para o S3")
async def create_kb(bucket_name: str, user_id: str, kb_id: str):
    use_case = SyncKbUseCase()
    controller = SyncKbController(use_case)
    params = {
        "bucket_name": bucket_name,
        "user_id": user_id,
        "kb_id": kb_id
    }
    request = HttpRequest(query_params=params)
    response = controller(request)

    if not response:
        raise HTTPException(
            status_code=500, detail="Algo deu errado ao sincronizar a base de conhecimento"
        )

    return response.data


@router.delete("/file", summary="Deleta um arquivo de uma base de conhecimento no S3")
async def delete_kb_file(bucket: str, user_id: str, kb_id: str, file_name: str):
    use_case = DeleteKbFileUseCase()
    controller = DeleteKbFileController(use_case)
    params = {
        "bucket": bucket,
        "user_id": user_id,
        "kb_id": kb_id,
        "file_name": file_name
    }
    request = HttpRequest(query_params=params)
    response = controller(request)

    if not response:
        raise HTTPException(
            status_code=500, detail="Algo deu errado ao deletar o arquivo da base de conhecimento"
        )

    return response.data
