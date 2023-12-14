import pathlib
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi import BackgroundTasks
from app.db import session
from app.db.crud import create_file_upload, uploaded_file_exists, delete_file_upload
from fastapi.responses import Response, FileResponse, StreamingResponse
from app.core.config import get_settings
from .core import upload_transcript, retrieve_transcript, upload_slide, retrieve_slide, S3Utils
from pydantic import BaseModel, HttpUrl
from loguru import logger
import hashlib 
import httpx 

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
        path (Path | str): Path to file in local storage
        url (HttpUrl | str): A URL for accessing the object.
        size (int): Size of the file in bytes.
        filename (str): Name of the file.
        status (bool): True if the upload is successful else False.
        error (str): Error message for failed upload.
        message: Response Message
    """
    path: str = ''
    url: HttpUrl | str = ''
    size: int = 0
    filename: str = ''
    content_type: str = ''
    status: bool = True
    error: str = ''
    message: str = ''

#TODO add to db as well     
@router.post("/uploadTranscript")
async def upload_lecture_transcript(req: TranscriptUploadModel, db= Depends(session.get_async_db)):
    userName = req.userName
    courseName = req.courseName
    videoName = req.videoName
    transcriptText = req.transcriptText
    settings = get_settings()
    
    courseName = str(courseName).lower().replace("-", "").replace(" ", "").strip()
    videoName = str(videoName).lower().replace(":", "").replace(" ", "-").strip() 
           
    logger.debug(f"User {userName} uploading transcript for {courseName} - {videoName}")       
    md5_hash = hashlib.md5(transcriptText.encode("utf-8")).hexdigest()
    if await uploaded_file_exists(db, md5_hash):
        result =  FileUploadResult(filename=f"{videoName}.txt",content_type=CONTENT_TYPE_MAP['.txt'], size=len(transcriptText),        
                                    status=False, error=f"File {videoName}.txt already exists!")
    else:
        file_url = await upload_transcript(courseName, videoName, transcriptText, settings)
        message = f"{courseName} - {videoName} transcript uploaded successfully."
        logger.info(message)
        filename=  file_url.split('/')[-1]
        result = FileUploadResult(url=file_url, message=message,
                                filename=filename, size=len(transcriptText),
                                content_type=CONTENT_TYPE_MAP['.txt'])
             
        await create_file_upload(db, course_id=courseName, course_name='', week_number='', lecture_number='',
                                lecture_title=videoName, source_url='', s3_url=file_url, file_name=filename,
                                doc_type='transcript', file_md5=md5_hash)
    return result 

@router.get("/retrieveTranscript/")
async def get_lecture_transcript(courseName: str, videoName: str, userName: str=''):
    logger.debug(f"{userName} requesting transcript for {courseName} - {videoName}")
    settings = get_settings()
    result = await retrieve_transcript(courseName, videoName, settings)
    logger.info(f"{courseName} - {videoName} transcript downloaded successfully.")
    # return StreamingResponse(result['Body'], media_type=CONTENT_TYPE_MAP['.txt'])
    return FileResponse(result['Body'], media_type=CONTENT_TYPE_MAP['.txt'], filename=f"{videoName}.txt")



async def calculate_md5(f: UploadFile):
    hasher = hashlib.md5()
    while True:
        chunk = await f.read(4096)
        if not chunk:
            break
        hasher.update(chunk)
    return hasher.hexdigest()

@router.post("/uploadSlide")
async def upload_lecture_slide(background_tasks: BackgroundTasks, 
                               courseName: str, slideFile: UploadFile,  videoName: str = '', userName: str='', 
                               db=Depends(session.get_async_db)):
    settings = get_settings()    
    try:
        courseName = str(courseName).lower().replace("-", "").replace(" ", "").strip()                             
        logger.debug(f"User {userName} uploading slide {slideFile.filename} for {courseName}")             
        md5_hash = await calculate_md5(slideFile)
        if await uploaded_file_exists(db, md5_hash):
            raise Exception(f"File {slideFile.filename} already exists!")
        # # # content_type = slideFile.content_type            
        file_type = pathlib.Path(slideFile.filename).suffix
        if file_type not in CONTENT_TYPE_MAP.keys():
            raise Exception(f'Unsupported file type: {slideFile.filename}. Supported types are {CONTENT_TYPE_MAP.keys()}')
        await slideFile.seek(0)
        folder_name = 'transcripts' if file_type in ['.txt'] else 'slides'
        file_url = await upload_slide(courseName, slideFile, settings, folder_name)
        
        message =  f'{slideFile.filename} uploaded successfully'
        logger.info(message)
        result = FileUploadResult(url=file_url, message=message, filename=slideFile.filename,
                                            content_type=slideFile.content_type, size=slideFile.size)           
        
        await create_file_upload(db, course_id=courseName, course_name='', week_number='', lecture_number='',
                                 lecture_title='', source_url='', s3_url=file_url, file_name=slideFile.filename,
                                 doc_type='slides', file_md5=md5_hash)

        if file_type in ['.txt']:
            s3_path = f"s3://{settings.S3_BUCKET_NAME}/{courseName}/{folder_name}/{slideFile.filename}"
            video_name = videoName if videoName else slideFile.filename
            background_tasks.add_task(call_generate_summary, courseName, video_name, s3_path)
    except Exception as e:
        logger.exception(e)
        result = FileUploadResult(filename=slideFile.filename,content_type=slideFile.content_type, size=slideFile.size,
                                    status=False, error=str(e))
    finally:
        await slideFile.close()
    return result


#TODO use asyncio.gather to upload multiple files
@router.post("/uploadSlides")
async def upload_lecture_slides(background_tasks: BackgroundTasks,
                                courseName: str, slideFiles: list[UploadFile], userName: str='', 
                                db=Depends(session.get_async_db)):
    settings = get_settings()
    results = []
    courseName = str(courseName).lower().replace("-", "").replace(" ", "").strip()                   
    for slideFile in slideFiles:        
        try:
            logger.debug(f"User {userName} uploading slide {slideFile.filename} for {courseName}")                 
            md5_hash = await calculate_md5(slideFile)
            if await uploaded_file_exists(db, md5_hash):
                raise Exception(f"File {slideFile.filename} already exists!")            
            # content_type = slideFile.content_type            
            file_type = pathlib.Path(slideFile.filename).suffix
            if file_type not in CONTENT_TYPE_MAP.keys():
                raise Exception(f'Unsupported file type: {slideFile.filename}. Supported types are {CONTENT_TYPE_MAP.keys()}')
            folder_name = 'transcripts' if file_type in ['.txt'] else 'slides'            
            await slideFile.seek(0)                            
            file_url = await upload_slide(courseName, slideFile, settings, folder_name)
            message =  f'{slideFile.filename} uploaded successfully'
            logger.info(message)
            result = FileUploadResult(url=file_url, message=message, filename=slideFile.filename,
                                                content_type=slideFile.content_type, size=slideFile.size)           

            await create_file_upload(db, course_id=courseName, course_name='', week_number='', lecture_number='',
                                 lecture_title='', source_url='', s3_url=file_url, file_name=slideFile.filename,
                                 doc_type='slide', file_md5=md5_hash)
            if file_type in ['.txt']:
                s3_path = f"s3://{settings.S3_BUCKET_NAME}/{courseName}/{folder_name}/{slideFile.filename}"
                video_name = slideFile.filename
                background_tasks.add_task(call_generate_summary, courseName, video_name, s3_path)
                            
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

@router.get("/listLectureMaterials")
def list_lecture_materials(courseName: str='', file_type='', userName: str = '', detail: bool = False):
    settings = get_settings()
    try:
        if not file_type or 'all' in str(file_type).lower():
            result = []
            for file_type in ['slides', 'transcripts']:
                result.extend(list_s3_bucket_contents(courseName, file_type, detail, settings))
            return result
        return list_s3_bucket_contents(courseName, file_type, detail, settings)
    except Exception as e:
        logger.error(e)


@router.delete("/removeCourseFile")
def remove_course_file(fileName: str, courseName: str = '', userName: str = '',
                       db=Depends(session.get_db)):
    settings = get_settings()
    try:
        import s3fs
        s3 = s3fs.S3FileSystem(anon=False,
                            key=settings.AWS_ACCESS_KEY_ID,
                            secret=settings.AWS_SECRET_ACCESS_KEY,
                            endpoint_url=settings.S3_ENDPOINT_URL,
                            ) 
        logger.info(fileName)
        logger.info(s3.exists(fileName))
        if s3.exists(fileName) and s3.isfile(fileName):
            logger.warning(f"Removing {fileName}")            
            s3_url = S3Utils.make_s3_url(fileName, settings.S3_ENDPOINT_URL)
            logger.info(s3_url)
            delete_file_upload(db, s3_url)
            s3.rm_file(fileName)            
            return f"{fileName} removed successfully!"        
        elif courseName:
            subfolder  = 'transcripts' if pathlib.Path(fileName).suffix in '.txt' else 'slides'
            filePath = f"{settings.S3_BUCKET_NAME}/{courseName}/{subfolder}/{fileName}"
            if s3.exists(filePath) and s3.isfile(filePath):
                logger.warning(f"Removing {filePath}")
                s3_url = S3Utils.make_s3_url(filePath, settings.S3_ENDPOINT_URL)
                logger.info(s3_url)
                delete_file_upload(db, s3_url)    
                s3.rm_file(filePath)                            
                return f"{courseName} file {fileName} removed successfully!"
        else:
            return f"{fileName} not found!"
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

def list_s3_bucket_contents(courseName, courseFolder, detail, settings):
    import s3fs
    s3 = s3fs.S3FileSystem(anon=False,
                        key=settings.AWS_ACCESS_KEY_ID,
                        secret=settings.AWS_SECRET_ACCESS_KEY,
                        endpoint_url=settings.S3_ENDPOINT_URL,
                        use_listings_cache = False,
                        )
    bucket_name = settings.S3_BUCKET_NAME
    if not courseName: 
        dirs= s3.glob(f"{bucket_name}/*/{courseFolder}/")
        results = []
        for d in dirs:
            course = d.split('/')[-2]
            files = s3.ls(f"{bucket_name}/{course}/{courseFolder}/", detail)
            results.extend(format_file_listing(files, course, courseFolder, detail, settings))
        return results
    else:
        files=  s3.ls(f"{bucket_name}/{courseName}/{courseFolder}/", detail)
        results= format_file_listing(files, courseName, courseFolder, detail, settings)
        return results
    

def format_file_listing(files, courseName, courseFolder, detail, settings):
    results = []
    for file in files:
        fn = file['Key'] if detail else file
        mydict = {"file": fn.split('/')[-1],
        "path":  S3Utils.make_s3_path(fn),
        "url":  S3Utils.make_s3_url(fn, settings.S3_ENDPOINT_URL),
        "course": courseName,
        "type": courseFolder
        }
        if detail: mydict.update(file)
        results.append( mydict)
    return results


def call_generate_summary(courseName, video_name , s3_path):
    # logger.info(courseName)
    # logger.info(video_name)
    # logger.info(s3_path)
    with httpx.Client() as client:
        response = client.post("https://cs410-pl7lwtg5za-uc.a.run.app/api/v1/summarization/generateSummary",
                              json=  {"userId" : 0, 
                                    "courseName": courseName,
                                    "videoName": video_name,
                                    "s3_path": s3_path,
                                    }, timeout=300)
        
        logger.info(response.json())
