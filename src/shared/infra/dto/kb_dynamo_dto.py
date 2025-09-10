from decimal import Decimal

from src.shared.domain.entities.knowledge_base import KnowledgeBase


class KnowledgeBaseDynamoDTO:
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str
    status: str
    documents_count: int
    categories: list[str]

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        created_at: str,
        updated_at: str,
        status: str,
        documents_count: int,
        categories: list[str],
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
        self.documents_count = documents_count
        self.categories = categories

    @staticmethod
    def from_entity(kb: KnowledgeBase) -> "KnowledgeBaseDynamoDTO":
        """
        Parse data from KnowledgeBase entity to KnowledgeBaseDynamoDTO
        """
        return KnowledgeBaseDynamoDTO(
            id=kb.id,
            name=kb.name,
            description=kb.description,
            created_at=kb.created_at,
            updated_at=kb.updated_at,
            status=kb.status,
            documents_count=kb.documents_count,
            categories=kb.categories,
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from KnowledgeBaseDynamoDTO to dict suitable for DynamoDB
        """
        return {
            "entity": "knowledge_base",
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "documents_count": Decimal(self.documents_count),
            "categories": self.categories,
        }

    @staticmethod
    def from_dynamo(item: dict) -> "KnowledgeBaseDynamoDTO":
        """
        Parse data from DynamoDB item to KnowledgeBaseDynamoDTO
        """
        return KnowledgeBaseDynamoDTO(
            id=item["id"],
            name=item["name"],
            description=item["description"],
            created_at=item["created_at"],
            updated_at=item["updated_at"],
            status=item["status"],
            documents_count=int(item["documents_count"]),
            categories=list(item.get("categories", [])),
        )

    def to_entity(self) -> KnowledgeBase:
        """
        Parse data from KnowledgeBaseDynamoDTO to KnowledgeBase entity
        """
        return KnowledgeBase(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            status=self.status,
            documents_count=self.documents_count,
            categories=self.categories,
        )

    def __repr__(self):
        return (
            f"KnowledgeBaseDynamoDTO("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"status={self.status!r}, "
            f"documents_count={self.documents_count}, "
            f"categories={self.categories!r}"
            f")"
        )

    def __eq__(self, other):
        if not isinstance(other, KnowledgeBaseDynamoDTO):
            return False
        return (
            self.id == other.id and
            self.name == other.name and
            self.description == other.description and
            self.created_at == other.created_at and
            self.updated_at == other.updated_at and
            self.status == other.status and
            self.documents_count == other.documents_count and
            self.categories == other.categories
        )

