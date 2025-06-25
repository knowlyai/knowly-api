from src.features.knowledge_base.interfaces.knowledge_base_repository_interface import (
    KnowledgeBaseRepositoryInterface,
)
from src.shared.domain.entities.knowledge_base import KnowledgeBase


class KnowledgeBaseRepositoryMock(KnowledgeBaseRepositoryInterface):
    mock_knowledge_bases: list[KnowledgeBase] = [
        KnowledgeBase(
            id="kb-001",
            name="Documentação da API",
            description="Base de conhecimento contendo toda a documentação da API",
            created_at="2025-06-20T10:00:00Z",
            updated_at="2025-06-23T15:30:00Z",
            status="active",
            documents_count=45,
            categories=["API", "Documentação", "Backend"],
        ),
        KnowledgeBase(
            id="kb-002",
            name="FAQ Clientes",
            description="Perguntas frequentes dos clientes e suas respostas",
            created_at="2025-06-21T08:00:00Z",
            updated_at="2025-06-23T12:00:00Z",
            status="active",
            documents_count=128,
            categories=["FAQ", "Atendimento", "Clientes"],
        ),
        KnowledgeBase(
            id="kb-003",
            name="Políticas Internas",
            description="Documentos de políticas e procedimentos internos",
            created_at="2025-06-19T14:00:00Z",
            updated_at="2025-06-22T16:45:00Z",
            status="draft",
            documents_count=23,
            categories=["Políticas", "RH", "Procedimentos"],
        ),
    ]

    async def get_by_id(self, id: str) -> KnowledgeBase | None:
        for kb in self.mock_knowledge_bases:
            if kb.id == id:
                return kb
        return None
