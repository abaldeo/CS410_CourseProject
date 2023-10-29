from langchain.document_loaders import S3FileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import openai
from botocore.exceptions import ClientError
from urllib.parse import urlparse
from typing import List
from pydantic import BaseModel
import os

AWS_REGION_NAME = os.getenv("REGION_NAME")
S3_ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

class SummaryRequestModel(BaseModel):
    userId: int
    courseName: str
    videoName: str
    S3Path: str

def get_transcript_from_s3(s3_path: str) -> List[Document]:
    parsed_s3 = urlparse(url=s3_path, allow_fragments=False)
    parsed_s3.path.lstrip('/')  # Internet implies this is generally a problem will need to verify
    loader = S3FileLoader(bucket=parsed_s3.netloc, key=parsed_s3.path, 
                          region_name=AWS_REGION_NAME, endpoint_url=S3_ENDPOINT_URL,
                          aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        return loader.load()
    except ClientError as error:
        # Handles if the s3 path dne
        return None

def check_cache(course_name: str, video_name: str) -> dict:
    return {"courseName": course_name, "videoName": video_name, "summary": "summary"}

def save_to_cache(course_name: str, video_name: str, summary: str):
    pass

def generate_summary(txt_to_summarize: Document):
    llm = openai()
    summary_chain = load_summarize_chain(llm=llm, chain_type="map_reduce")
    return summary_chain.run(txt_to_summarize)

def write_summary_to_db():
    pass
