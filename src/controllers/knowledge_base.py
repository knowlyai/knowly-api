from fastapi import APIRouter, HTTPException
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_controller import GetPresignedBucketUrlController
from src.modules.get_presigned_bucket_url.app.get_presigned_bucket_url_usecase import GetPresignedBucketUrlUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.functions.generate_presigned_bucket_url import generate_presigned_bucket_url

router = APIRouter(prefix="/kb", tags=["Knowledge Bases"])


@router.get("/upload-files", summary="Enviar arquivos para a base de conhecimento")
async def upload_files(bucket: str, user_id: str, kb_id: str, expires: int = 900, max_size_mb: int = 20):
    params = generate_presigned_bucket_url(
        bucket=bucket,
        prefix=f"{user_id}/{kb_id}/",
        expires=expires,
        max_size_mb=max_size_mb
    )
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
            status_code=500, detail="Erro ao gerar URL pré-assinada"
        )

    return response.data
