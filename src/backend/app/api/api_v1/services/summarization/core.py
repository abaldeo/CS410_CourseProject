from langchain.document_loaders import S3FileLoader
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from redis import Redis
import boto3
import botocore
import asyncio

from typing import List
import os

from app.api.api_v1.utils.text_splitting import clean_text

AWS_REGION_NAME = os.getenv("REGION_NAME")
S3_ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

class SummaryRequestModel(BaseModel):
    userId: int
    courseName: str
    videoName: str
    S3Path: str


# Helper function to upload a transcript
async def upload_summary_to_s3(course_name: str, transcript_name: str, summary_text: str):
    """Writes the generated summary to a database

    Args:
        course_name (str): course video is associated with
        transcript_name (str): video's transcript that's being summarized
        summary_text (str): Summary of transcript
    """
    loop = asyncio.get_event_loop()

    def upload_summary(course_name: str, transcript_name: str, summary_text: str):
        session = boto3.session.Session()
        client = session.client('s3',
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                region_name='nyc3',
                                endpoint_url='https://nyc3.digitaloceanspaces.com',
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        # Define the object key (file path)
        object_key = f"{course_name}/{transcript_name}.txt"

        # Upload the transcript text to DigitalOcean Spaces
        client.put_object(Bucket="coursebuddysummary",
                          Key=object_key,
                          Body=summary_text,
                          ACL='private',
                          Metadata={
                              'x-amz-meta-my-key': 'placeholder-value'
                          })

    await loop.run_in_executor(None, upload_summary, course_name, transcript_name, summary_text)

def get_transcript_from_s3(s3_path: str) -> List[Document]:
    """Retrieves the text transcript of a video from s3

    Args:
        s3_path (str): Amazon s3 path to access transcript 

    Returns:
        List[Document]: List of one Document object that is the transcript for a specific video
    """
    parsed_s3 = urlparse(url=s3_path, allow_fragments=False)
    parsed_s3.path.lstrip('/')
    loader = S3FileLoader(bucket=parsed_s3.netloc, key=parsed_s3.path, 
                          region_name=AWS_REGION_NAME, endpoint_url=S3_ENDPOINT_URL,
                          aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        return loader.load()
    except ClientError:
        # Handles if the s3 path DNE
        return None

def check_cache(course_name: str, video_name: str, redis_instance: Redis) -> dict:
    """_summary_

    Args:
        course_name (str): course video is associated with
        video_name (str): video's transcript that's being summarized
        redis_instance (Redis): redis instance for caching
    Returns:
        dict: Returns summary and metadata 
    """
    cache_key = f"{course_name}/{video_name}"
    if redis_instance.exists(cache_key):
        return {
            "courseName": course_name, 
            "videoName": video_name, 
            "summary": redis_instance.hget(cache_key)
            }
    else:
        return None

def save_to_cache(course_name: str, video_name: str, summary: str, redis_instance: Redis) -> None:
     """Saves generated summary to a cache for easy access

     Args:
        course_name (str): course video is associated with
        video_name (str): video's transcript that's being summarized
        summary (str): Summary of transcript
        redis_instance (Redis): redis instance for caching
     """
     redis_instance.hset(key=f"{course_name}/{video_name}", value=summary)

def generate_summary(txt_to_summarize: Document) -> str:
    """Uses an LLM to generate a summary for a transcript

    Args:
        txt_to_summarize (Document): The transcript to summarize

    Returns:
        str: Returns summarization of the transcript
    """
    cleaned_txt = clean_text(txt_to_summarize.page_content)
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    template="""
    Compose a concise and a brief summary of the following text:
    TEXT: `{text}`
    Give the summary in bullet points using a max of {num_bullet_points} concise bullet points.
    """
    # TODO come up with logic to decide max bullet points
    prompt = PromptTemplate(
        input_variables=['text', 'num_bullet_points'],
        template=template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    bulleted_summary= chain.run({'text':cleaned_txt, 'num_bullet_points':'8'})
    return bulleted_summary


