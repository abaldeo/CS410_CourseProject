import boto3
import botocore
import os
import requests
import pathlib
import aioboto3



# Helper function to upload a transcript
async def upload_transcript(course_name, transcript_name, transcript_text):
        session = aioboto3.Session()
        client = session.client('s3',
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                region_name=os.getenv('REGION_NAME'),
                                endpoint_url=os.getenv('ENDPOINT_URL'),
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

        # Define the object key (file path)
        object_key = f"{course_name}/{transcript_name}.txt"

        # Upload the transcript text to DigitalOcean Spaces
        await client.put_object(Bucket=os.getenv('S3_BUCKET_NAME'),
                          Key=object_key,
                          Body=transcript_text,
                          ACL='private',
                          Metadata={
                              'x-amz-meta-my-key': 'placeholder-value'
                          })
        return f"Transcript {transcript_name} for course {course_name} uploaded successfully."


# Helper function to retrieve a transcript
async def retrieve_transcript(course_name, transcript_name):
        # Define the object key (file path)
        object_key = f"{course_name}/{transcript_name}.txt"
        session = aioboto3.Session()
        client = session.client('s3',
                                # Configures to use subdomain/virtual calling format.
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                region_name=os.getenv('REGION_NAME'),
                                endpoint_url=os.getenv('ENDPOINT_URL'),
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

        #Retrieve the transcript text from DigitalOcean Spaces
        await client.download_file(os.getenv('S3_BUCKET_NAME'),
                        object_key,
                        './object_key') #This saves the file to a literally ./object_key and needs to be figured out
        return "File downloaded successfully!"


# Helper function to upload a slide deck (.ppt, .pdf)
async def upload_slides(course_name, transcript_name, slide_file):
        session = aioboto3.Session()
        client = session.client('s3',
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                region_name=os.getenv('REGION_NAME'),
                                endpoint_url=os.getenv('ENDPOINT_URL'),
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

        # Define the object key (file path)
        object_key = f"{course_name}/{transcript_name}"

        # Get the file extension to ensure it is in the correct format
        file_extension = pathlib.Path(slide_file).suffix

        if file_extension in [".pdf", ".ppt"]:
            # Upload the PDF or PPT slide to DigitalOcean Spaces
            await client.put_object(Bucket=os.getenv('S3_BUCKET_NAME'),
                            Key=object_key + file_extension,
                            Body=slide_file,
                            ACL='private',
                            Metadata={'x-amz-meta-my-key': 'placeholder-value'})
            return f"Slide deck {transcript_name} for course {course_name} uploaded successfully."
        else:
            return f"Unsupported file format: {file_extension}. Slide deck not uploaded."


# Helper function to retrieve a transcript
async def retrieve_slides(course_name, slide_name):
        session = aioboto3.Session()
        client = session.client('s3',
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                region_name=os.getenv('REGION_NAME'),
                                endpoint_url=os.getenv('ENDPOINT_URL'),
                                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

        # Attempt to retrieve a ".pdf" version of the file
        pdf_object_key = f"{course_name}/{slide_name}.pdf"
        try:
            local_pdf_file_path = f'./{slide_name}.pdf'
            await client.download_file(os.getenv('S3_BUCKET_NAME'), pdf_object_key, local_pdf_file_path)
            return f"File {slide_name}.pdf downloaded successfully."
        except Exception as pdf_error:
            # If a ".pdf" version is not found, attempt to retrieve a ".ppt" version of the file
            ppt_object_key = f"{course_name}/{slide_name}.ppt"
            try:
                local_ppt_file_path = f'./{slide_name}.ppt'
                await client.download_file(os.getenv('S3_BUCKET_NAME'), ppt_object_key, local_ppt_file_path)
                return f"File {slide_name}.ppt downloaded successfully."
            except Exception as ppt_error:
                return f"Failed to download file {slide_name}.pdf or {slide_name}.ppt. Error: {str(pdf_error) if 'pdf' in str(pdf_error) else str(ppt_error)}"



#Uploads all text files in a directory 
def upload_transcript_test():
    directory = "/workspaces/CS410_CourseProject/src/backend/data/transcripts"
    endpoint_url = "https://cuddly-space-cod-4vgggj7vpg53jg65-8000.app.github.dev/api/docs#/file_upload/uploadTranscriptTester_api_v1_file_upload_uploadTranscriptTest_post"

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # Check if it is a file and ends with '.txt'
        if os.path.isfile(f) and filename.endswith('.txt'):
            with open(f, 'r') as text_file:
                text = text_file.read()

            # Set up the data to be sent in the POST request
            data = {
                "course_name": "CS410",  # Replace with your course name
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