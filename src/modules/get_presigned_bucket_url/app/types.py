from typing import TypedDict


class PresignedPostFields(TypedDict):
    key: str
    AWSAccessKeyId: str
    policy: str
    signature: str


class PresignedPostResponse(TypedDict):
    url: str
    fields: PresignedPostFields

class GetPresignedBucketUrlRequest(TypedDict):
    bucket: str
    user_id: str
    kb_id: str
    expires: int
    max_size_mb: int
