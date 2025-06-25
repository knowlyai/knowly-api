from src.features.knowledge_base.interfaces.get_knowledge_base_use_case_interface import (
    GetKnowledgeBaseInterface,
)
from src.features.knowledge_base.interfaces.knowledge_base_repository_interface import (
    KnowledgeBaseRepositoryInterface,
)
from src.shared.domain.entities.knowledge_base import KnowledgeBase


class GetKnowledgeBase(GetKnowledgeBaseInterface):
    def __init__(self, knowledge_base_repository: KnowledgeBaseRepositoryInterface):
        self.knowledge_base_repository = knowledge_base_repository

    async def execute(self, knowledge_base_id: str) -> KnowledgeBase | None:
        return await self.knowledge_base_repository.get_by_id(knowledge_base_id)
