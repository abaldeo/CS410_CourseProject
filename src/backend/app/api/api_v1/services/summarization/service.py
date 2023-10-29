from fastapi import APIRouter
from langchain.docstore.document import Document
from typing import List
from .core import check_cache, save_to_cache, write_summary_to_db, get_transcript_from_s3, SummaryRequestModel

router = APIRouter()

@router.get("/fetchSummary")
async def fetchSummary(courseName: str, videoName: str) -> dict:
    """Given a course name and video name check the cache to see if we have a summary already generated

    Args:
        courseName (str): Name of course the video comes from
        videoName (str): The video for which the transcript we want to summarize

    Returns:
        dict: Summary results or None
    """
    cache_results: dict | None = check_cache(courseName, videoName)
    if cache_results:
        return cache_results
    else:
        return {}  # Do we want explicit not found or is {} sufficient

@router.post("/generateSummary")
async def generateSummary(summary_model: SummaryRequestModel) -> dict:
    """ 
    Given an s3 path to a video transcript, load the transcript, summarize it using the llm, save the results to the cache
    and database, and return the results.

    Args:
        summary_model (SummaryRequestModel): Input data from the http request

    Returns:
        dict: The summary of the transcript and some meta data or an error that the summary could not be generated
    """
    transcripts_to_summarize: List[Document] | None = get_transcript_from_s3(s3_path=summary_model.S3Path,)
    if transcripts_to_summarize:
        summary_result = generateSummary(transcripts_to_summarize[0]) # Assuming only one doc
        save_to_cache(course_name=summary_model.courseName, video_name=summary_model.videoName, summary=summary_result)
        write_summary_to_db()
        result = {"summary": summary_result}
        result.update(summary_model.json())
        return result
    else:
        return {"error": f"Could not generate summary for video: {summary_model.videoName} in course: {summary_model.courseName}"}
    




