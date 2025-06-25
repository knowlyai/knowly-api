from abc import abstractmethod
from src.shared.domain.entities.knowledge_base import KnowledgeBase


class GetKnowledgeBaseInterface:
    @abstractmethod
    async def execute(self, knowledge_base_id: str) -> KnowledgeBase | None:
        pass
