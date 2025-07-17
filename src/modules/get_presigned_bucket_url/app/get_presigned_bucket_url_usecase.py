from src.modules.get_presigned_bucket_url.app.generate_presigned_bucket_url import generate_presigned_bucket_url
from src.modules.get_presigned_bucket_url.app.types import PresignedPostResponse


class GetPresignedBucketUrlUseCase:
    def __call__(self, bucket: str, user_id: str, kb_id: str, expires: int = 900, max_size_mb: int = 20) -> PresignedPostResponse:
        return generate_presigned_bucket_url(
            bucket=bucket,
            prefix=f"{user_id}/{kb_id}/",
            expires=expires,
            max_size_mb=max_size_mb
        )
