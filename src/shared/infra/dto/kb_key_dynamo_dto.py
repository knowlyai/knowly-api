from src.shared.domain.entities.kb_key import KbKey


class KbKeyDynamoDTO:
    user_id: str
    kb_id: str
    kb_key: str
    kb_key_alias: str

    def __init__(
        self,
        user_id: str,
        kb_id: str,
        kb_key: str,
        kb_key_alias: str,
    ):
        self.user_id = user_id
        self.kb_id = kb_id
        self.kb_key = kb_key
        self.kb_key_alias = kb_key_alias

    @staticmethod
    def from_entity(kb_key: KbKey) -> "KbKeyDynamoDTO":
        return KbKeyDynamoDTO(
            user_id=kb_key.user_id,
            kb_id=kb_key.kb_id,
            kb_key=kb_key.kb_key,
            kb_key_alias=kb_key.kb_key_alias,
        )

    def to_dynamo(self) -> dict:
        return {
            "entity": "kb_key",
            "user_id": self.user_id,
            "kb_id": self.kb_id,
            "kb_key": self.kb_key,
            "kb_key_alias": self.kb_key_alias,
        }

    @staticmethod
    def from_dynamo(item: dict) -> "KbKeyDynamoDTO":
        return KbKeyDynamoDTO(
            user_id=item["user_id"],
            kb_id=item["kb_id"],
            kb_key=item["kb_key"],
            kb_key_alias=item["kb_key_alias"],
        )

    def to_entity(self) -> KbKey:
        return KbKey(
            user_id=self.user_id,
            kb_id=self.kb_id,
            kb_key=self.kb_key,
            kb_key_alias=self.kb_key_alias,
        )

