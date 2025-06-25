from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

from src.features.knowledge_base.repositories.knowledge_base_repository import (
    KnowledgeBaseRepositoryMock,
)
from src.features.knowledge_base.use_cases.get_knowledge_base_use_case import (
    GetKnowledgeBase,
)

router = APIRouter(prefix="/knowledge-bases", tags=["Knowledge Base"])

# @router.get("/", summary="Listar todas as bases de conhecimento")
# async def get_all_knowledge_bases(
#     status: Optional[str] = None,
#     category: Optional[str] = None,
#     limit: int = 10,
#     offset: int = 0,
# ):
#     """
#     Retorna todas as bases de conhecimento com filtros opcionais.

#     - **status**: Filtrar por status (active, draft, archived)
#     - **category**: Filtrar por categoria
#     - **limit**: Número máximo de resultados
#     - **offset**: Número de registros a pular
#     """
#     filtered_kbs = mock_knowledge_bases.copy()

#     # Aplicar filtros
#     if status:
#         filtered_kbs = [kb for kb in filtered_kbs if kb["status"] == status]

#     if category:
#         filtered_kbs = [kb for kb in filtered_kbs if category in kb["categories"]]

#     # Aplicar paginação
#     paginated_kbs = filtered_kbs[offset : offset + limit]

#     return {
#         "data": paginated_kbs,
#         "total": len(filtered_kbs),
#         "limit": limit,
#         "offset": offset,
#     }


@router.get("/{kb_id}", summary="Obter uma base de conhecimento específica")
async def get_knowledge_base(kb_id: str):
    repository = KnowledgeBaseRepositoryMock()
    use_case = GetKnowledgeBase(repository)
    kb = await use_case.execute(kb_id)

    if not kb:
        raise HTTPException(
            status_code=404, detail="Base de conhecimento não encontrada"
        )

    return kb


# @router.post("/", summary="Criar nova base de conhecimento")
# async def create_knowledge_base(
#     name: str, description: str, categories: List[str] = []
# ):
#     """
#     Cria uma nova base de conhecimento.
#     """
#     new_kb = {
#         "id": f"kb-{len(mock_knowledge_bases) + 1:03d}",
#         "name": name,
#         "description": description,
#         "created_at": datetime.now().isoformat() + "Z",
#         "updated_at": datetime.now().isoformat() + "Z",
#         "status": "draft",
#         "documents_count": 0,
#         "categories": categories,
#     }

#     mock_knowledge_bases.append(new_kb)

#     return {"data": new_kb, "message": "Base de conhecimento criada com sucesso"}


# @router.put("/{kb_id}", summary="Atualizar base de conhecimento")
# async def update_knowledge_base(
#     kb_id: str,
#     name: Optional[str] = None,
#     description: Optional[str] = None,
#     status: Optional[str] = None,
#     categories: Optional[List[str]] = None,
# ):
#     """
#     Atualiza uma base de conhecimento existente.
#     """
#     kb_index = next(
#         (i for i, kb in enumerate(mock_knowledge_bases) if kb["id"] == kb_id), None
#     )

#     if kb_index is None:
#         raise HTTPException(
#             status_code=404, detail="Base de conhecimento não encontrada"
#         )

#     kb = mock_knowledge_bases[kb_index]

#     # Atualizar campos se fornecidos
#     if name is not None:
#         kb["name"] = name
#     if description is not None:
#         kb["description"] = description
#     if status is not None:
#         kb["status"] = status
#     if categories is not None:
#         kb["categories"] = categories

#     kb["updated_at"] = datetime.now().isoformat() + "Z"

#     return {"data": kb, "message": "Base de conhecimento atualizada com sucesso"}


# @router.delete("/{kb_id}", summary="Deletar base de conhecimento")
# async def delete_knowledge_base(kb_id: str):
#     """
#     Remove uma base de conhecimento.
#     """
#     kb_index = next(
#         (i for i, kb in enumerate(mock_knowledge_bases) if kb["id"] == kb_id), None
#     )

#     if kb_index is None:
#         raise HTTPException(
#             status_code=404, detail="Base de conhecimento não encontrada"
#         )

#     deleted_kb = mock_knowledge_bases.pop(kb_index)

#     return {
#         "data": {"id": deleted_kb["id"]},
#         "message": "Base de conhecimento deletada com sucesso",
#     }


# @router.get(
#     "/{kb_id}/documents", summary="Listar documentos de uma base de conhecimento"
# )
# async def get_knowledge_base_documents(kb_id: str, limit: int = 10, offset: int = 0):
#     """
#     Retorna os documentos de uma base de conhecimento específica.
#     """
#     kb = next((kb for kb in mock_knowledge_bases if kb["id"] == kb_id), None)

#     if not kb:
#         raise HTTPException(
#             status_code=404, detail="Base de conhecimento não encontrada"
#         )

#     # Mock documents
#     mock_documents = [
#         {
#             "id": f"doc-{i+1:03d}",
#             "title": f"Documento {i+1}",
#             "content": f"Conteúdo do documento {i+1} da base {kb['name']}",
#             "created_at": "2025-06-23T10:00:00Z",
#             "updated_at": "2025-06-23T15:30:00Z",
#         }
#         for i in range(kb["documents_count"])
#     ]

#     paginated_docs = mock_documents[offset : offset + limit]

#     return {
#         "data": paginated_docs,
#         "total": len(mock_documents),
#         "knowledge_base_id": kb_id,
#         "limit": limit,
#         "offset": offset,
#     }


# @router.post("/{kb_id}/search", summary="Buscar na base de conhecimento")
# async def search_knowledge_base(kb_id: str, query: str, limit: int = 5):
#     """
#     Busca por conteúdo dentro de uma base de conhecimento específica.
#     """
#     kb = next((kb for kb in mock_knowledge_bases if kb["id"] == kb_id), None)

#     if not kb:
#         raise HTTPException(
#             status_code=404, detail="Base de conhecimento não encontrada"
#         )

#     # Mock search results
#     mock_results = [
#         {
#             "document_id": "doc-001",
#             "title": f"Resultado sobre '{query}' - Documento 1",
#             "snippet": f"Este é um trecho relevante sobre {query} encontrado no documento...",
#             "relevance_score": 0.95,
#             "url": f"/knowledge-bases/{kb_id}/documents/doc-001",
#         },
#         {
#             "document_id": "doc-045",
#             "title": f"Resultado sobre '{query}' - Documento 2",
#             "snippet": f"Outro trecho importante relacionado a {query} que pode ser útil...",
#             "relevance_score": 0.87,
#             "url": f"/knowledge-bases/{kb_id}/documents/doc-045",
#         },
#     ]

#     return {
#         "data": mock_results[:limit],
#         "query": query,
#         "knowledge_base_id": kb_id,
#         "total_results": len(mock_results),
#     }
