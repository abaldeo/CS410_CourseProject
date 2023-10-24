from fastapi import APIRouter
from .core import upload_transcript, retrieve_transcript
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
    return upload_transcript(courseName, videoName, transcriptText)

@router.post("/uploadSlides")
async def uploadSlides(uploadModel: UploadModel):
    return uploadModel

@router.get("/transcripts/{courseName}/{videoName}")
async def getTranscript(courseName: str, videoName: str):
    return retrieve_transcript(courseName, videoName)

@router.get("/slides/{courseName}/{slideName}")
async def getSlides(uploadModel: UploadModel):
    return uploadModel.fileObject