from fastapi import APIRouter
from . import service

embedding_router = APIRouter(prefix="/embedding", tags=["embedding"])
embedding_router.include_router(service.router)