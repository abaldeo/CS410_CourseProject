from fastapi import APIRouter

from .embedding import embedding_router

from .summarization import summarization_router

from .file_upload import file_upload_router

service_router = APIRouter()
service_router.include_router(embedding_router)
service_router.include_router(summarization_router)
service_router.include_router(file_upload_router)
