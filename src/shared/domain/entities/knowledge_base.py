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
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
        self.documents_count = documents_count
        self.categories = categories

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
        }

    def __repr__(self):
        return f"KnowledgeBase(id={self.id}, name={self.name}, status={self.status})"
