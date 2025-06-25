from abc import abstractmethod
from typing import Optional
from src.shared.domain.entities.knowledge_base import KnowledgeBase


class KnowledgeBaseRepositoryInterface:
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[KnowledgeBase]:
        pass

    @abstractmethod
    def create(self, entity: KnowledgeBase):
        pass

    @abstractmethod
    def update(self, id: str, data: KnowledgeBase):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass
