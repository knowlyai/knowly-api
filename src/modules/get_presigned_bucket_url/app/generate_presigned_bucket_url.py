from dotenv import load_dotenv
import os
import boto3

from src.modules.get_presigned_bucket_url.app.types import PresignedPostResponse

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION_NAME')
)


def generate_presigned_bucket_url(
        bucket: str,
        prefix: str,
        expires: int = 900,
        max_size_mb: int = 20
) -> PresignedPostResponse:
    response = s3.generate_presigned_post(
        Bucket=bucket,
        Key=f"{prefix.rstrip('/')}/${{filename}}",
        ExpiresIn=expires,
        Conditions=[
            ["starts-with", "$key", prefix],
            ["content-length-range", 1, max_size_mb * 1024 * 1024]
        ]
    )
    return response
