import pytest

from src.shared.domain.entities.knowledge_base import KnowledgeBase
from src.shared.helpers.errors.domain_errors import EntityError


class TestKnowledgeBase:
    def _make_kb(self, kb_id: str, name: str = "MinhaKB") -> KnowledgeBase:
        return KnowledgeBase(
            id=kb_id,
            name=name,
            description="Descrição",
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:00:00Z",
            status="ACTIVE",
            documents_count=0,
            categories=["geral"],
        )

    def test_kb_with_valid_id(self):
        kb = self._make_kb("A1b2C3d4E5")
        assert kb.id == "A1b2C3d4E5"

    @pytest.mark.parametrize(
        "invalid_id",
        [
            None,  # none
            1234567890,  # not a string
            "123456789",  # 9 chars
            "12345678901",  # 11 chars
            "Abcde-1234",  # invalid char '-'
            "Abcde_1234",  # invalid char '_'
            "ábcdEF1234",  # accented char
            "abc def123",  # space
        ],
    )
    def test_kb_with_invalid_id_raises_entity_error(self, invalid_id):
        with pytest.raises(EntityError):
            self._make_kb(invalid_id)

    @pytest.mark.parametrize(
        "valid_name",
        [
            "A",
            "A_",
            "Z9-",
            "AbCdEf",
            "A_B-C_D",
            ("a_" * 100).rstrip("_") + "_",  # exatamente 100 repetições do padrão
        ],
    )
    def test_kb_with_valid_name(self, valid_name):
        kb = self._make_kb("A1b2C3d4E5", name=valid_name)
        assert kb.name == valid_name

    @pytest.mark.parametrize(
        "invalid_name",
        [
            None,
            123,
            "",  # vazio
            " ",  # espaço
            "_abc",  # começa com _
            "-abc",  # começa com -
            "abc ",  # espaço no fim
            "ab c",  # espaço no meio
            "a__",  # dois separadores seguidos não obedecem ao padrão do grupo
            "a--",
            "a_b-.",  # ponto não permitido
            ("a_" * 101),  # 101 repetições excedem {1,100}
        ],
    )
    def test_kb_with_invalid_name_raises_entity_error(self, invalid_name):
        with pytest.raises(EntityError):
            self._make_kb("A1b2C3d4E5", name=invalid_name)
