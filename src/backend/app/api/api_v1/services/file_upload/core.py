import boto3
import botocore
import os


session = boto3.session.Session()
client = session.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                        region_name=os.getenv('REGION_NAME'),
                        endpoint_url=os.getenv('ENDPOINT_URL'),
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

# Helper function to upload a transcript
def upload_transcript(course_name, transcript_name, transcript_text):
    # Define the object key (file path)
    object_key = f"{course_name}/{transcript_name}.txt"

    # Upload the transcript text to DigitalOcean Spaces
    client.put_object(Bucket="coursebuddy",
                  Key=object_key,
                  Body=transcript_text,
                  ACL='private',
                  Metadata={
                      'x-amz-meta-my-key': 'placeholder-value'
                  }
                )
    return f"Transcript {transcript_name} for course {course_name} uploaded successfully."

# Helper function to retrieve a transcript
def retrieve_transcript(course_name, transcript_name):
    # Define the object key (file path)
    object_key = f"{course_name}/{transcript_name}.txt"

    try:
        # Retrieve the transcript text from DigitalOcean Spaces
        transcript_text = client.download_file('coursebuddy',
                     object_key,
                     # This is a placeholder, need to set a standard location for file to be downloaded
                     '/Users/coltonbailey/Downloads/test_bucket_downloaded.py')
        return transcript_text
    except Exception as e:
        return f"Error: Transcript {transcript_name} for course {course_name} not found."


# Helper function to upload a transcript
# def upload_transcript(course_name: str, transcript_name: str, transcript_text: str):
#     # Define the object key (file path)
#     object_key = f"{course_name}/{transcript_name}.txt"

#     # Upload the transcript text to DigitalOcean Spaces
#     # s3.put_object(Bucket=DO_SPACES_BUCKET_NAME, Key=object_key, Body=transcript_text)
#     client.put_object(Bucket=DO_SPACES_BUCKET_NAME,
#                   Key=f"str(transcript_name).txt",
#                   Body=transcript_text,
#                   ACL='private',
#                   Metadata={
#                       'x-amz-meta-my-key': 'placeholder-value'
#                   }
#                 )
#     return f"Transcript {transcript_name} for course {course_name} uploaded successfully."

# # Helper function to retrieve a transcript
# def retrieve_transcript(course_name: str, transcript_name: str):
#     # Define the object key (file path)
#     object_key = f"{course_name}/{transcript_name}.txt"

#     try:
#         # Retrieve the transcript text from DigitalOcean Spaces
#         response = s3.get_object(Bucket=DO_SPACES_BUCKET_NAME, Key=object_key)
#         transcript_text = response['Body'].read().decode('utf-8')
#         return transcript_text
#     except Exception as e:
#         return f"Error: Transcript {transcript_name} for course {course_name} not found."
    
