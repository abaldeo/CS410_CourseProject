from fastapi import FastAPI
from fastapi import APIRouter
import uvicorn

from app.core import config
# from .service import router
# from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Should we move this to another file?
class SummaryModel(BaseModel):
    userId: int
    courseName: str
    videoName: str
    S3Path: str

@router.get("/fetchSummary")
async def fetchSummary(courseName: str, videoName: str):
    # TODO implement
    return {"summary": f"This will contain a summary for video '{videoName}' from the course '{courseName}' "}

@router.post("/generateSummary")
async def generateSummary(summary_model: SummaryModel):
    return summary_model



summarization_router = APIRouter(prefix="/summarization", tags=["summarization"])
summarization_router.include_router(router)


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)

app.include_router(summarization_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
    