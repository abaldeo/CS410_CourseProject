from fastapi import APIRouter
from . import service

rag_router = APIRouter(prefix="/rag", tags=["rag"])
rag_router.include_router(service.router)