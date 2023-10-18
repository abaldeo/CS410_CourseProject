from fastapi import FastAPI, UploadFile, File
import boto3
import os

# Initialize the DigitalOcean Spaces client
s3 = boto3.client('s3',
                  region_name='nyc3',
                  endpoint_url=DO_SPACES_ENDPOINT_URL,
                  aws_access_key_id=DO_SPACES_ACCESS_KEY,
                  aws_secret_access_key=DO_SPACES_SECRET_KEY)


# Helper function to upload a transcript
def upload_transcript(course_name: str, transcript_name: str, transcript_text: str):
    # Define the object key (file path)
    object_key = f"{course_name}/{transcript_name}.txt"

    # Upload the transcript text to DigitalOcean Spaces
    s3.put_object(Bucket=DO_SPACES_BUCKET_NAME, Key=object_key, Body=transcript_text)

    return f"Transcript {transcript_name} for course {course_name} uploaded successfully."

# Helper function to retrieve a transcript
def retrieve_transcript(course_name: str, transcript_name: str):
    # Define the object key (file path)
    object_key = f"{course_name}/{transcript_name}.txt"

    try:
        # Retrieve the transcript text from DigitalOcean Spaces
        response = s3.get_object(Bucket=DO_SPACES_BUCKET_NAME, Key=object_key)
        transcript_text = response['Body'].read().decode('utf-8')
        return transcript_text
    except Exception as e:
        return f"Error: Transcript {transcript_name} for course {course_name} not found."
    
