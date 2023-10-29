from fastapi import APIRouter
from . import service

summarization_router = APIRouter(prefix="/summarization", tags=["summarization"])
summarization_router.include_router(service.router)