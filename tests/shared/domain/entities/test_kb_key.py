import pytest

from src.shared.domain.entities.kb_key import KbKey
from src.shared.helpers.errors.domain_errors import EntityError


class TestKbKey:
    def _make_kb_key(
        self,
        user_id: str = "user123",
        kb_id: str = "A1b2C3d4E5",
        kb_key: str = "sk_test_key123456",
        kb_key_alias: str = "production_key",
    ) -> KbKey:
        return KbKey(
            user_id=user_id,
            kb_id=kb_id,
            kb_key=kb_key,
            kb_key_alias=kb_key_alias,
        )

#a
    def test_kb_key_with_valid_attributes(self):
        kb_key = self._make_kb_key()
        assert kb_key.user_id == "user123"
        assert kb_key.kb_id == "A1b2C3d4E5"
        assert kb_key.kb_key == "sk_test_key123456"
        assert kb_key.kb_key_alias == "production_key"

    @pytest.mark.parametrize(
        "invalid_user_id",
        [
            None,
            123,
            "",
        ],
    )
    def test_kb_key_with_invalid_user_id_raises_entity_error(self, invalid_user_id):
        with pytest.raises(EntityError):
            self._make_kb_key(user_id=invalid_user_id)

    @pytest.mark.parametrize(
        "invalid_kb_id",
        [
            None,
            1234567890,
            "123456789",  # 9 chars
            "12345678901",  # 11 chars
            "Abcde-1234",  # invalid char '-'
            "Abcde_1234",  # invalid char '_'
            "´bcdEF1234",  # accented char
            "abc def123",
            "",
        ],
    )
    def test_kb_key_with_invalid_kb_id_raises_entity_error(self, invalid_kb_id):
        with pytest.raises(EntityError):
            self._make_kb_key(kb_id=invalid_kb_id)

    @pytest.mark.parametrize(
        "invalid_kb_key",
        [
            None,
            123,
            "",
        ],
    )
    def test_kb_key_with_invalid_kb_key_raises_entity_error(self, invalid_kb_key):
        with pytest.raises(EntityError):
            self._make_kb_key(kb_key=invalid_kb_key)

    @pytest.mark.parametrize(
        "invalid_kb_key_alias",
        [
            None,
            123,
            "",
        ],
    )
    def test_kb_key_with_invalid_kb_key_alias_raises_entity_error(self, invalid_kb_key_alias):
        with pytest.raises(EntityError):
            self._make_kb_key(kb_key_alias=invalid_kb_key_alias)

    def test_kb_key_to_dict(self):
        kb_key = self._make_kb_key()
        result = kb_key.to_dict()
        assert result == {
            "user_id": "user123",
            "kb_id": "A1b2C3d4E5",
            "kb_key": "sk_test_key123456",
            "kb_key_alias": "production_key",
        }

    def test_kb_key_repr(self):
        kb_key = self._make_kb_key()
        result = repr(kb_key)
        assert result == "KbKey(user_id=user123, kb_id=A1b2C3d4E5, kb_key_alias=production_key)"
