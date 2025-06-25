from fastapi import FastAPI
from src.controllers.knowledge_base import router as knowledge_base_router
from src.controllers.user import router as user_router

app = FastAPI(
    title="Knowly API",
    description="API para gerenciamento de bases de conhecimento e usuários.",
    version="1.0.0",
)

# Knowledge Bases
app.include_router(knowledge_base_router)
app.include_router(user_router)
