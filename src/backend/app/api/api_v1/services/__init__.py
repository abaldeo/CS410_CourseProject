from fastapi import APIRouter

from .embedding import embedding_router


service_router = APIRouter()
service_router.include_router(embedding_router)