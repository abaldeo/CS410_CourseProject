from fastapi import APIRouter
from .core import upload_transcript_async, retrieve_transcript_async, upload_transcript_test, upload_slides_async, retrieve_slides_async
from pydantic import BaseModel
router = r = APIRouter()

class UploadModel(BaseModel):
    userId: int
    courseName: str
    videoName: str
    transcriptText: str
    fileName: str
    fileObject: object

@router.post("/uploadTranscript")
async def uploadTranscript(userId: str, courseName: str, videoName: str, transcriptText: str):
    await upload_transcript_async(courseName, videoName, transcriptText)

@router.post("/uploadSlides")
async def uploadSlides(course_name: str, transcript_name: str, slide_object: object):
    await upload_slides_async(course_name, transcript_name, slide_object)

@router.get("/transcripts/{courseName}/{videoName}")
async def getTranscript(courseName: str, videoName: str):
    await retrieve_transcript_async(courseName, videoName)

@router.get("/slides/{courseName}/{slideName}")
async def getSlides(course_name: str, slide_name: str):
    await retrieve_slides_async(course_name, slide_name)

@router.post("/uploadTranscriptTest")
async def uploadTranscriptTester():
    return upload_transcript_test()