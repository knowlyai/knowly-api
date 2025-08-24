from typing import TypedDict


class SyncKbRequest(TypedDict):
    bucket_name: str
    user_id: str
    kb_id: str
