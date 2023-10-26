from fastapi import FastAPI
from fastapi import APIRouter
import uvicorn

from app.core import config
from .service import router


router = APIRouter()


file_upload_router = APIRouter(prefix="/file_upload", tags=["file_upload"])
file_upload_router.include_router(router)


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

app.include_router(file_upload_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)