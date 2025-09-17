import re
from src.shared.helpers.errors.domain_errors import EntityError


class KnowledgeBase:
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
        if not KnowledgeBase.validate_id(id):
            raise EntityError("id")
        self.id = id
        if not KnowledgeBase.validate_name(name):
            raise EntityError("name")
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
    def validate_id(value: str) -> bool:
        if value is None or type(value) is not str:
            return False
        pattern = re.compile(r"^[0-9A-Za-z]{10}$")
        return bool(pattern.fullmatch(value))

    @staticmethod
    def validate_name(value: str) -> bool:
        if value is None or type(value) is not str:
            return False
        pattern = re.compile(r"^([0-9A-Za-z][_-]?){1,100}$")
        return bool(pattern.fullmatch(value))

    def to_dict(self):
        """Converte o objeto KnowledgeBase para dicionário"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "documents_count": self.documents_count,
            "categories": self.categories,
            "display_name": self.display_name,
            "rds_table": self.rds_table,
        }

    def __repr__(self):
        return f"KnowledgeBase(id={self.id}, name={self.name}, status={self.status}, display_name={self.display_name}, rds_table={self.rds_table})"
