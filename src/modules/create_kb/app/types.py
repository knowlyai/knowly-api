from typing import TypedDict


class CreateKbRequest(TypedDict):
    kb_name: str
    kb_description: str
    kb_display_name: str
