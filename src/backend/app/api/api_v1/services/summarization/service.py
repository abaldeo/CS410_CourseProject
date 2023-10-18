from fastapi import APIRouter
from pydantic import BaseModel
from .core import check_cache, get_video_transcript, generate_summary

router = APIRouter()

# Should we move this to another file?
class SummaryRequestModel(BaseModel):
    userId: int
    courseName: str
    videoName: str
    S3Path: str

class Summary(BaseModel):
    courseName: str
    videoName: str
    summary: str

@router.get("/fetchSummary")
async def fetchSummary(courseName: str, videoName: str) -> Summary:
    cache_results: None | Summary = check_cache(courseName, videoName)
    if cache_results:
        return cache_results
    else:
        transcripts_to_summarize = get_video_transcript(courseName, videoName)
        summary: Summary = generate_summary(transcripts_to_summarize)
        return summary

@router.post("/generateSummary")
async def generateSummary(summary_model: SummaryRequestModel):
    # TODO implement
    return {"summary_model": "model"}




