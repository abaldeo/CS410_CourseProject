import pathlib
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import Response, FileResponse, StreamingResponse
from app.core.config import get_settings
from .core import upload_transcript, retrieve_transcript, upload_slide, retrieve_slide
from pydantic import BaseModel, HttpUrl
from loguru import logger
router = r = APIRouter()

SUPPORTED_FILE_TYPES = ['.pdf', '.ppt', '.pptx']
CONTENT_TYPE_MAP = {'.pdf':'application/pdf', 
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx':'application/vnd.ms-powerpoint',
            '.txt': 'text/plain'}

class FileUploadModel(BaseModel):
    userName: str = ''
    courseName: str
    videoName: str
    slideFile: list[UploadFile]

class TranscriptUploadModel(BaseModel):
    userName: str = ''
    courseName: str
    videoName: str
    transcriptText: str

class FileUploadResult(BaseModel):
    """
    Represents the result of an upload operation

    Attributes:
        file (Bytes): File saved to memory
        path (Path | str): Path to file in local storage
        url (HttpUrl | str): A URL for accessing the object.
        size (int): Size of the file in bytes.
        filename (str): Name of the file.
        status (bool): True if the upload is successful else False.
        error (str): Error message for failed upload.
        message: Response Message
    """
    file: bytes = b''
    path: str = ''
    url: HttpUrl | str = ''
    size: int = 0
    filename: str = ''
    content_type: str = ''
    status: bool = True
    error: str = ''
    message: str = ''
    
@router.post("/uploadTranscript")
async def upload_lecture_transcript(req: TranscriptUploadModel):
    userName = req.userName
    courseName = req.courseName
    videoName = req.videoName
    transcriptText = req.transcriptText
    settings = get_settings()
    logger.debug(f"User {userName} uploading transcript for {courseName} - {videoName}")      
    result = await upload_transcript(courseName, videoName, transcriptText, settings)
    logger.info(f"{courseName} - {videoName} transcript uploaded successfully.")
    return result 

@router.get("/retrieveTranscript/")
async def get_lecture_transcript(courseName: str, videoName: str, userName: str=''):
    logger.debug(f"{userName} requesting transcript for {courseName} - {videoName}")
    settings = get_settings()
    result = await retrieve_transcript(courseName, videoName, settings)
    logger.info(f"{courseName} - {videoName} transcript downloaded successfully.")
    # return StreamingResponse(result['Body'], media_type=CONTENT_TYPE_MAP['.txt'])
    return FileResponse(result['Body'], media_type=CONTENT_TYPE_MAP['.txt'], filename=f"{videoName}.txt")


@router.post("/uploadSlide")
async def upload_lecture_slide(courseName: str, slideFile: UploadFile,  videoName: str = '', userName: str=''):
    settings = get_settings()
    try:
        # content_type = slideFile.content_type            
        file_type = pathlib.Path(slideFile.filename).suffix
        if file_type not in CONTENT_TYPE_MAP.keys():
            raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Unsupported file type: {slideFile.filename}. Supported types are {CONTENT_TYPE_MAP.keys()}'
                        )
        file_url = await upload_slide(courseName, slideFile, settings)
        message =  f'{slideFile.filename} uploaded successfully'
        logger.info(message)
        result = FileUploadResult(url=file_url, message=message, filename=slideFile.filename,
                                            content_type=slideFile.content_type, size=slideFile.size)           

    except Exception as e:
        logger.exception(e)
        result = FileUploadResult(filename=slideFile.filename,content_type=slideFile.content_type, size=slideFile.size,
                                    status=False, error=str(e))
    finally:
        await slideFile.close()
    return result


#TODO use asyncio.gather to upload multiple files
@router.post("/uploadSlides")
async def upload_lecture_slides(courseName: str, slideFiles: list[UploadFile], userName: str=''):
    settings = get_settings()
    results = []
    for slideFile in slideFiles:        
        try:
            # content_type = slideFile.content_type            
            file_type = pathlib.Path(slideFile.filename).suffix
            if file_type not in CONTENT_TYPE_MAP.keys():
                raise HTTPException(
                                status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Unsupported file type: {slideFile.filename}. Supported types are {CONTENT_TYPE_MAP.keys()}'
                            )
            file_url = await upload_slide(courseName, slideFile, settings)
            message =  f'{slideFile.filename} uploaded successfully'
            logger.info(message)
            result = FileUploadResult(url=file_url, message=message, filename=slideFile.filename,
                                                content_type=slideFile.content_type, size=slideFile.size)           

        except Exception as e:
            logger.exception(e)
            result = FileUploadResult(filename=slideFile.filename,content_type=slideFile.content_type, size=slideFile.size,
                                      status=False, error=str(e))
        finally:
            await slideFile.close()
        results.append(result)
    return results 



@router.get("/retrieveSlide")
async def get_lecture_slide(courseName: str, slideFileName: str, userName: str = ''):
    settings = get_settings()  
    # result = retrieve_slides(course_name, slide_name)    
    file_type = pathlib.Path(slideFileName).suffix    
    try:
        result = await retrieve_slide(courseName, slideFileName, settings)
        if not result:
            raise HTTPException(status_code=404, detail="File not found for {courseName} - {slideName}!")
        return FileResponse(result['Body'], media_type=CONTENT_TYPE_MAP[file_type], filename=slideFileName)
        # return StreamingResponse(result['Body'], 
                                #  media_type='application/octet-stream',
                                #  headers={"Content-Disposition": f"attachment;filename={slideFileName}"})
        
    except Exception as e:
        logger.exception(e)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listSlides")
def list_lecture_slides(courseName: str='', userName: str = '', detail: bool = False):
    settings = get_settings()
    try:
        return list_s3_bucket_contents(courseName, 'slides', detail, settings)
    except Exception as e:
        logger.error(e)


@router.get("/listTranscripts")
def list_lecture_slides(courseName: str='', userName: str = '', detail: bool = False):
    settings = get_settings()
    try:
        return list_s3_bucket_contents(courseName, 'transcripts', detail, settings)
    except Exception as e:
        logger.error(e)

@router.delete("/removeCourseFile")
def remove_course_file(fileName: str, courseName: str = '', userName: str = ''):
    settings = get_settings()
    try:
        import s3fs
        s3 = s3fs.S3FileSystem(anon=False,
                            key=settings.AWS_ACCESS_KEY_ID,
                            secret=settings.AWS_SECRET_ACCESS_KEY,
                            endpoint_url=settings.S3_ENDPOINT_URL,
                            ) 
        if s3.exists(fileName) and s3.isfile(fileName):
            logger.warning(f"Removing {fileName}")            
            s3.rm_file(fileName)
            return f"{fileName} removed successfully!"        
        elif courseName:
            subfolder  = 'transcripts' if pathlib.Path(fileName).suffix in '.txt' else 'slides'
            filePath = f"{settings.S3_BUCKET_NAME}/{courseName}/{subfolder}/{fileName}"
            if s3.exists(filePath) and s3.isfile(filePath):
                logger.warning(f"Removing {filePath}")
                s3.rm_file(filePath)
                return f"{courseName} file {fileName} removed successfully!"
        else:
            return f"{fileName} not found!"
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

def list_s3_bucket_contents(courseName, courseFolder, detail, settings):
    import s3fs
    s3 = s3fs.S3FileSystem(anon=False,
                        key=settings.AWS_ACCESS_KEY_ID,
                        secret=settings.AWS_SECRET_ACCESS_KEY,
                        endpoint_url=settings.S3_ENDPOINT_URL,
                        )
    bucket_name = settings.S3_BUCKET_NAME
    if not courseName: 
        dirs= s3.glob(f"{bucket_name}/*/{courseFolder}/")
        results = []
        for dir in dirs:
            course = dir.split('/')[-2]
            results.extend(s3.ls(f"{bucket_name}/{course}/{courseFolder}/", detail))
        return results
    else:
        return  s3.ls(f"{bucket_name}/{courseName}/{courseFolder}/", detail)