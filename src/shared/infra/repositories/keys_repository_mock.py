from typing import List

from src.shared.domain.entities.kb_key import KbKey
from src.shared.domain.repositories.keys_repository_interface import IKeysRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class KeysRepositoryMock(IKeysRepository):
    kb_keys: List[KbKey]

    def __init__(self):
        self.kb_keys = [
            KbKey(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                kb_id="A1B2C3D4E5",
                kb_key="mock_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
                kb_key_alias="Production API Key"
            ),
            KbKey(
                user_id="fdddafb9-687a-4982-a025-54fb12671932",
                kb_id="A1B2C3D4E5",
                kb_key="mock_test_z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4",
                kb_key_alias="Test API Key"
            ),
            KbKey(
                user_id="5042b518-83ca-4cbf-84fc-c992da2506e5",
                kb_id="123456ABCD",
                kb_key="mock_live_9f8e7d6c5b4a3e2d1c0b9a8f7e6d5c4b",
                kb_key_alias="IMT Main Key"
            ),
            KbKey(
                user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
                kb_id="abcDEF1234",
                kb_key="mock_live_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
                kb_key_alias="TechCorp Primary"
            ),
            KbKey(
                user_id="f7e6d5c4-b3a2-9180-7654-321098765432",
                kb_id="abcDEF1234",
                kb_key="mock_dev_q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6",
                kb_key_alias="TechCorp Development"
            ),
        ]

    def create_kb_key(self, kb_key: KbKey) -> KbKey:
        self.kb_keys.append(kb_key)
        return kb_key

    def get_kb_keys(self, user_id: str, kb_id: str = None) -> List[KbKey]:
        if kb_id:
            keys = [key for key in self.kb_keys if key.user_id == user_id and key.kb_id == kb_id]
            return keys
        return [key for key in self.kb_keys if key.user_id == user_id]

    def delete_kb_key(self, user_id: str, kb_key: str) -> KbKey:
        for idx, key in enumerate(self.kb_keys):
            if key.user_id == user_id and key.kb_key == kb_key:
                return self.kb_keys.pop(idx)
        raise NoItemsFound("kb_key")

    def get_kb_id_by_key(self, kb_key: str) -> str:
        for key in self.kb_keys:
            if key.kb_key == kb_key:
                return key.kb_id
        raise NoItemsFound("kb_key")
