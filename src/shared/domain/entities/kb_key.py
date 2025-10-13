import re
from src.shared.helpers.errors.domain_errors import EntityError


class KbKey:
    def __init__(
        self,
        user_id: str,
        kb_id: str,
        kb_key: str,
        kb_key_alias: str,
    ):
        if not KbKey.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id
        if not KbKey.validate_kb_id(kb_id):
            raise EntityError("kb_id")
        self.kb_id = kb_id
        if not KbKey.validate_kb_key(kb_key):
            raise EntityError("kb_key")
        self.kb_key = kb_key
        if not KbKey.validate_kb_key_alias(kb_key_alias):
            raise EntityError("kb_key_alias")
        self.kb_key_alias = kb_key_alias

    @staticmethod
    def validate_user_id(value: str) -> bool:
        if value is None or type(value) is not str:
            return False
        return len(value) > 0

    @staticmethod
    def validate_kb_id(value: str) -> bool:
        if value is None or type(value) is not str:
            return False
        pattern = re.compile(r"^[0-9A-Za-z]{10}$")
        return bool(pattern.fullmatch(value))

    @staticmethod
    def validate_kb_key(value: str) -> bool:
        if value is None or type(value) is not str:
            return False
        return len(value) > 0

    @staticmethod
    def validate_kb_key_alias(value: str) -> bool:
        if value is None or type(value) is not str:
            return False
        return len(value) > 0

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "kb_id": self.kb_id,
            "kb_key": self.kb_key,
            "kb_key_alias": self.kb_key_alias,
        }

    def __repr__(self):
        return f"KbKey(user_id={self.user_id}, kb_id={self.kb_id}, kb_key_alias={self.kb_key_alias})"