

from langchain.docstore.document import Document
from fastapi import APIRouter
import functools
import redis

from typing import List

from .core import check_cache, save_to_cache, upload_summary_to_s3, get_transcript_from_s3, SummaryRequestModel
from app.core.config import settings


router = APIRouter()

@functools.lru_cache()
def get_redis_instance(): 
    redis_client = redis.Redis(host=settings.SUMM_REDIS_HOST, 
                               port=settings.SUMM_REDIS_PORT, 
                               password=settings.SUMM_REDIS_PASSWD)
    return redis_client

REDIS_INSTANCE = get_redis_instance()

@router.get("/fetchSummary")
async def fetchSummary(courseName: str, videoName: str) -> dict:
    """Given a course name and video name check the cache to see if we have a summary already generated

    Args:
        courseName (str): Name of course the video comes from
        videoName (str): The video for which the transcript we want to summarize

    Returns:
        dict: Summary results or None
    """
    cache_results: dict | None = check_cache(courseName=courseName, video_name=videoName, 
                                             redis_instance=REDIS_INSTANCE)
    if cache_results:
        return cache_results
    else:
        return {}  # Do we want explicit not found or is {} sufficient

@router.post("/generateSummary")
async def generateSummary(summary_model: SummaryRequestModel) -> dict:
    """ 
    Given an s3 path to a video transcript, load the transcript, summarize it using the llm, save the results to the 
    cache and database, and return the results.

    Args:
        summary_model (SummaryRequestModel): Input data from the http request

    Returns:
        dict: The summary of the transcript and some meta data or an error that the summary could not be generated
    """
    transcripts_to_summarize: List[Document] | None = get_transcript_from_s3(s3_path=summary_model.S3Path,)
    if transcripts_to_summarize:
        summary_result = generateSummary(transcripts_to_summarize[0]) # Assuming only one doc
        save_to_cache(course_name=summary_model.courseName, video_name=summary_model.videoName, summary=summary_result, 
                      redis_instance=REDIS_INSTANCE)
        upload_summary_to_s3(course_name=summary_model.courseName, transcript_name=summary_model.videoName,
                              summary_text=summary_result)
        result = {
            "summary": summary_result
            }
        result.update(summary_model.json())
        return result
    else:
        return {
            "error": f"Could not generate summary for video: {summary_model.videoName} in course: " 
            f"{summary_model.courseName}"
            }
    
