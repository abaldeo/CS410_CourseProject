from fastapi import APIRouter
from . import service

file_upload_router = APIRouter(prefix="/file_upload", tags=["file_uplaod"])
file_upload_router.include_router(service.router)