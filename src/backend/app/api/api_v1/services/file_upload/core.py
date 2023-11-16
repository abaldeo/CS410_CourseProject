import botocore
import os
import aioboto3
from loguru import logger
from app.core.config import get_settings
import tempfile  

class S3Utils:
    @staticmethod
    def get_client(region_name:str = '', s3_endpoint_url:str = '', 
                   aws_access_key_id:str= '', aws_secret_access_key:str = ''
                   ):
        settings = get_settings()
        region_name = region_name or settings.AWS_REGION_NAME
        s3_endpoint_url= s3_endpoint_url or settings.S3_ENDPOINT_URL
        aws_access_key_id = aws_access_key_id or settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = aws_secret_access_key or settings.AWS_SECRET_ACCESS_KEY
        session = aioboto3.Session() 
        client = session.client(
            's3', 
            config=botocore.config.Config(s3={'addressing_style': 'virtual'}), 
            region_name=region_name,
            endpoint_url=s3_endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        return client 
    
    @staticmethod 
    async def upload_to_s3(bucket_name: str, s3_path: str, text: str, client = None, metadata = {}):
        """Uploads a file to an S3 bucket"""  
        client =S3Utils.get_client()
        async with client as s3: 
            result = await s3.put_object(
                Bucket=bucket_name, 
                Key=s3_path, 
                Body=text, 
                ACL='public-read', 
                Metadata=metadata
            )
            logger.debug(result)
            return result 

    @staticmethod
    async def download_from_s3(bucket_name: str, s3_path: str, client = None):
        """Downloads a file from an S3 bucket"""
        client =S3Utils.get_client()
        async with client as s3: 
            result =  await s3.get_object(Bucket=bucket_name, Key=s3_path)

            logger.debug(result)
            result['Body']= await S3Utils.read_stream_to_temp_file(result['Body'])
            return result
  
    
    @staticmethod
    async def file_exists_in_s3(bucket_name: str, object_key: str, client = None) -> bool:
        client =S3Utils.get_client()
        async with client as s3: 
            try:
                await s3.head_object(Bucket=bucket_name, Key=object_key)
                return True  # File exists
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    return False  # File does not exist
                else:
                    raise  # Other error
            
    @staticmethod
    async def read_stream_to_temp_file(stream):
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_path = temp_file.name

        # Write the contents of the StreamingBody to the temporary file
        with open(temp_path, 'wb') as f:
            while True:
                chunk = await stream.read(1024)
                if not chunk:
                    break
                f.write(chunk)

        return temp_path
                        
                
async def upload_transcript(course_name, transcript_name, transcript_text, settings):
    aws_region_name= settings.AWS_REGION_NAME
    s3_endpoint_url=  settings.S3_ENDPOINT_URL
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY        
    s3_bucket = settings.S3_BUCKET_NAME    
    course_name = str(course_name).lower().replace("-", "").replace(" ", "").strip()
    transcript_name = str(transcript_name).lower().replace(":", "").replace(" ", "-").strip()  
    metadata = {
        'x-amz-meta-course-name': course_name,
        'x-amz-meta-lecture-title': transcript_name,
        'x-amz-meta-lecture-url': ''
    }
    object_key = f"{course_name}/transcripts/{transcript_name}.txt"
    # client = S3Utils.get_client(aws_region_name, s3_endpoint_url, aws_access_key_id, aws_secret_access_key)        
    logger.info(f"Uploading {object_key} to bucket {s3_bucket}")
    result = await S3Utils.upload_to_s3(s3_bucket, object_key, transcript_text, metadata=metadata)
    return result 


async def retrieve_transcript(course_name, transcript_name, settings):
    aws_region_name= settings.AWS_REGION_NAME
    s3_endpoint_url=  settings.S3_ENDPOINT_URL
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY
    s3_bucket = settings.S3_BUCKET_NAME 
    course_name = str(course_name).lower().replace("-", "").replace(" ", "").strip()
    transcript_name = str(transcript_name).lower().replace(":", "").replace(" ", "-").strip()
    object_key = f"{course_name}/transcripts/{transcript_name}.txt"
    # client = S3Utils.get_client(aws_region_name, s3_endpoint_url, aws_access_key_id, aws_secret_access_key)        
    logger.info(f"Downloading {object_key} from bucket {s3_bucket}")
    result = await S3Utils.download_from_s3(s3_bucket, object_key)
    return result



async def upload_slide(course_name, slide_file, settings):
    aws_region_name= settings.AWS_REGION_NAME
    s3_endpoint_url=  settings.S3_ENDPOINT_URL
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY        
    s3_bucket = settings.S3_BUCKET_NAME     
    course_name = str(course_name).lower().replace("-", "").replace(" ", "").strip()   
    object_key = f"{course_name}/slides/{slide_file.filename}"
    metadata = {
        'x-amz-meta-course-name': course_name,
        'x-amz-meta-lecture-title': slide_file.filename,
        'x-amz-meta-lecture-url': '',
        'x-amz-meta-content-type': slide_file.content_type,
        'x-amz-meta-size': str(slide_file.size)
        
    }
    # client = S3Utils.get_client(aws_region_name, s3_endpoint_url, aws_access_key_id, aws_secret_access_key)            
    contents = await slide_file.read()
    logger.info(f"Uploading {object_key} to bucket {s3_bucket}")
    result = await S3Utils.upload_to_s3(s3_bucket, object_key, contents, metadata=metadata)
    file_url = f"{s3_endpoint_url}/{s3_bucket}/{object_key}"
    return file_url 

 
 
async def retrieve_slide(course_name, slide_file_name, settings):
    aws_region_name= settings.AWS_REGION_NAME
    s3_endpoint_url=  settings.S3_ENDPOINT_URL
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY        
    s3_bucket = settings.S3_BUCKET_NAME       
    course_name = str(course_name).lower().replace("-", "").replace(" ", "").strip()       
    object_key = f"{course_name}/slides/{slide_file_name}"        
    # client = S3Utils.get_client(aws_region_name, s3_endpoint_url, aws_access_key_id, aws_secret_access_key)   
    logger.info(f"Checking {object_key} exists in bucket {s3_bucket}")             
    if await S3Utils.file_exists_in_s3(s3_bucket, object_key):
        logger.info(f"Downloading {object_key} from S3 {s3_bucket}")
        response = await S3Utils.download_from_s3(s3_bucket, object_key)
        return response
    else:
        logger.warning(f" {object_key} not found in bucket {s3_bucket}!")
        return None 


def test_upload_slides():
    from fastapi.testclient import TestClient
    from app.api.api_v1.services.file_upload.main import app    
    client = TestClient(app)
    directory = "/workspaces/CS410_CourseProject/src/backend/data/slides"        
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Check if it is a file and ends with '.txt'
        if os.path.isfile(f) and filename.endswith('.pdf'):
            file =  open(f, 'rb')
            resp = client.post("/uploadSlide?courseName=cs410", 
                            files={"slideFile": (filename,file , "application/pdf")},
                            )
            file.close()
            print(resp.content)

def test_upload_transcripts():
    from fastapi.testclient import TestClient
    from app.api.api_v1.services.file_upload.main import app    
    client = TestClient(app)
    directory = "/workspaces/CS410_CourseProject/src/backend/data/transcripts"        
    
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Check if it is a file and ends with '.txt'
        if os.path.isfile(f) and filename.endswith('.txt'):
            with open(f, 'rb') as file:
                videoName = filename.replace(".txt", "")    
                resp = client.post("/uploadTranscript", 
                                json={"courseName": "cs410", "videoName": videoName, 
                                      "transcriptText": file.read().decode("utf-8")},)
                print(resp.content)

      
if __name__ == '__main__':
    test_upload_transcripts()
#    test_upload_slides()
