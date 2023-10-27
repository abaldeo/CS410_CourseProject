import boto3
import botocore
import os
import requests

# session = boto3.session.Session()
# client = session.client('s3',
#                         config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
#                         region_name=os.getenv('AWS_REGION_NAME'),
#                         endpoint_url=os.getenv('S3_ENDPOINT_URL'),
#                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
#                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

# Helper function to upload a transcript
def upload_transcript(course_name, transcript_name, transcript_text):
    print("============================================")
    print(os.getenv('REGION_NAME'))
    print(os.getenv('ENDPOINT_URL'))
    print(os.getenv('AWS_ACCESS_KEY_ID'))
    print(os.getenv('AWS_SECRET_ACCESS_KEY'))
    print("============================================")
    session = boto3.session.Session()
    client = session.client('s3',
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                            region_name='nyc3',#os.getenv('AWS_REGION_NAME'),
                            endpoint_url='https://nyc3.digitaloceanspaces.com',#os.getenv('S3_ENDPOINT_URL'),
                            aws_access_key_id='DO0034NULEWCYM7L9XDV',#os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key='98I7DEe8D/swjS8vpgchlJw2WXIATb/fIaEBZb3PFYk')#os.getenv('AWS_SECRET_ACCESS_KEY'))

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
    session = boto3.session.Session()
    client = session.client('s3',
                            config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                            region_name='nyc3',#os.getenv('AWS_REGION_NAME'),
                            endpoint_url='https://nyc3.digitaloceanspaces.com',#os.getenv('S3_ENDPOINT_URL'),
                            aws_access_key_id='DO0034NULEWCYM7L9XDV',#os.getenv('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key='98I7DEe8D/swjS8vpgchlJw2WXIATb/fIaEBZb3PFYk')#os.getenv('AWS_SECRET_ACCESS_KEY'))
    #try:
    print("=====================")
    print(object_key)
    print("=====================")

        # Retrieve the transcript text from DigitalOcean Spaces
    transcript_text = client.download_file('coursebuddy',
                    object_key,
                    './object_key')
    return "File downloaded successfully!"
    #except Exception as e:
    #return f"Error: Transcript {transcript_name} for course {course_name} not found."


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
    
#Uploads all text files in a directory 
# !! Not working yet !!
def upload_transcript_test():
    directory = "/workspaces/CS410_CourseProject/src/backend/data/transcripts"
    endpoint_url = "https://cuddly-space-cod-4vgggj7vpg53jg65-8000.app.github.dev/api/docs#/file_upload/uploadTranscriptTester_api_v1_file_upload_uploadTranscriptTest_post"  # Replace with your actual endpoint URL

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Check if it is a file and ends with '.txt'
        if os.path.isfile(f) and filename.endswith('.txt'):
            with open(f, 'r') as text_file:
                text = text_file.read()

            # Set up the data to be sent in the POST request
            data = {
                "course_name": "CS411",  # Replace with your course name
                "transcript_name": filename,
                "transcript_text": text
            }

            # Send the POST request to the FastAPI endpoint
            response = requests.post(endpoint_url, data=data)

            # Check the response
            if response.status_code == 200:
                print(f"Transcript {filename} uploaded successfully.")
            else:
                print(f"Failed to upload transcript {filename}. Status code: {response.status_code}")