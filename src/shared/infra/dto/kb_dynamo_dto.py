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
    display_name: str
    rds_table: str

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
        display_name: str,
        rds_table: str,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
        self.documents_count = documents_count
        self.categories = categories
        self.display_name = display_name
        self.rds_table = rds_table

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
            display_name=kb.display_name,
            rds_table=kb.rds_table,
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
            "display_name": self.display_name,
            "rds_table": self.rds_table,
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
            display_name=item.get("display_name", item.get("name", "")),
            rds_table=item.get("rds_table", ""),
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
            documents_count=int(str(self.documents_count)),
            categories=self.categories,
            display_name=self.display_name,
            rds_table=self.rds_table,
        )

    def __repr__(self):
        return (
            f"KnowledgeBaseDynamoDTO("
            f"id={self.id!r}, name={self.name!r}, status={self.status!r}, "
            f"documents_count={self.documents_count}, categories={self.categories!r}, "
            f"display_name={self.display_name!r}, rds_table={self.rds_table!r})"
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
            self.categories == other.categories and
            self.display_name == other.display_name and
            self.rds_table == other.rds_table
        )
