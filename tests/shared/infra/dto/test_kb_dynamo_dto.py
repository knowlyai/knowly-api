from decimal import Decimal

from src.shared.domain.entities.knowledge_base import KnowledgeBase
from src.shared.infra.dto.kb_dynamo_dto import KnowledgeBaseDynamoDTO
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestKnowledgeBaseDynamoDTO:
    def test_from_entity(self):
        repo = UserRepositoryMock()
        kb = repo.kbs[0]

        dto = KnowledgeBaseDynamoDTO.from_entity(kb)

        expected = KnowledgeBaseDynamoDTO(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            created_at=kb.created_at,
            updated_at=kb.updated_at,
            status=kb.status,
            documents_count=kb.documents_count,
            categories=kb.categories,
        )

        assert dto == expected

    def test_to_dynamo(self):
        repo = UserRepositoryMock()
        kb = repo.kbs[0]

        dto = KnowledgeBaseDynamoDTO.from_entity(kb)
        item = dto.to_dynamo()

        expected = {
            "entity": "knowledge_base",
            "id": kb.id,
            "name": kb.name,
            "description": kb.description,
            "created_at": kb.created_at,
            "updated_at": kb.updated_at,
            "status": kb.status,
            "documents_count": Decimal(kb.documents_count),
            "categories": kb.categories,
        }

        assert item == expected

    def test_from_dynamo(self):
        dynamo_item = {
            "entity": "knowledge_base",
            "id": "A1B2C3D4E5",
            "name": "KB_Principal",
            "description": "Base principal de conhecimento",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-02T00:00:00Z",
            "status": "ACTIVE",
            "documents_count": Decimal("2"),
            "categories": ["geral", "produtos"],
        }

        dto = KnowledgeBaseDynamoDTO.from_dynamo(dynamo_item)

        expected = KnowledgeBaseDynamoDTO(
            id="A1B2C3D4E5",
            name="KB_Principal",
            description="Base principal de conhecimento",
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-02T00:00:00Z",
            status="ACTIVE",
            documents_count=2,
            categories=["geral", "produtos"],
        )

        assert dto == expected

    def test_from_dynamo_without_categories(self):
        dynamo_item = {
            "entity": "knowledge_base",
            "id": "123456ABCD",
            "name": "KB-SemCats",
            "description": "Sem categorias",
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
            "status": "INACTIVE",
            "documents_count": Decimal("0"),
            # sem 'categories'
        }

        dto = KnowledgeBaseDynamoDTO.from_dynamo(dynamo_item)

        assert dto.categories == []
        assert dto.documents_count == 0

    def test_to_entity(self):
        dto = KnowledgeBaseDynamoDTO(
            id="abcDEF1234",
            name="KB_3",
            description="Terceira base de conhecimento",
            created_at="2025-02-01T00:00:00Z",
            updated_at="2025-02-01T00:00:00Z",
            status="ACTIVE",
            documents_count=5,
            categories=["faq"],
        )

        kb = dto.to_entity()

        assert isinstance(kb, KnowledgeBase)
        assert kb.id == "abcDEF1234"
        assert kb.name == "KB_3"
        assert kb.description == "Terceira base de conhecimento"
        assert kb.created_at == "2025-02-01T00:00:00Z"
        assert kb.updated_at == "2025-02-01T00:00:00Z"
        assert kb.status == "ACTIVE"
        assert kb.documents_count == 5
        assert kb.categories == ["faq"]

    def test_from_dynamo_to_entity(self):
        dynamo_item = {
            "entity": "knowledge_base",
            "id": "A1b2C3d4E5",
            "name": "KB_Principal",
            "description": "Base principal",
            "created_at": "2025-03-01T00:00:00Z",
            "updated_at": "2025-03-02T00:00:00Z",
            "status": "ACTIVE",
            "documents_count": Decimal("3"),
            "categories": ["a", "b"],
        }

        dto = KnowledgeBaseDynamoDTO.from_dynamo(dynamo_item)
        kb = dto.to_entity()

        expected = KnowledgeBase(
            id="A1b2C3d4E5",
            name="KB_Principal",
            description="Base principal",
            created_at="2025-03-01T00:00:00Z",
            updated_at="2025-03-02T00:00:00Z",
            status="ACTIVE",
            documents_count=3,
            categories=["a", "b"],
        )

        assert kb.id == expected.id
        assert kb.name == expected.name
        assert kb.description == expected.description
        assert kb.created_at == expected.created_at
        assert kb.updated_at == expected.updated_at
        assert kb.status == expected.status
        assert kb.documents_count == expected.documents_count
        assert kb.categories == expected.categories

