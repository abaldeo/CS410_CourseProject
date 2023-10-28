import os
from app.api.api_v1.services.embedding.core import load_s3_file
import boto3
import botocore
from dotenv import load_dotenv
load_dotenv()

REGION_NAME = os.getenv("REGION_NAME")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")

print(REGION_NAME)
print(ENDPOINT_URL)
print(AWS_SECRET_ACCESS_KEY)
print(AWS_ACCESS_KEY_ID)


session = boto3.session.Session()
client = session.client('s3',
                        config=botocore.config.Config(s3={'addressing_style': 'virtual'}), # Configures to use subdomain/virtual calling format.
                        region_name=REGION_NAME,
                        endpoint_url=ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

#lists all buckets in account
response = client.list_buckets()
for space in response['Buckets']:
    print(space['Name'])
    bucket_name = space['Name']

#prints all files in coursebuddy bucket
response = client.list_objects(Bucket=bucket_name)
for obj in response['Contents']:
    print(obj['Key'])

# #puts a file named file.text in bucket. Change the name of the file name to upload another file, then re-run this script to see that it got uploaded
# client.put_object(Bucket=bucket_name,
#                   Key='file.text',
#                   Body=b'The contents of the file.',
#                   ACL='private',
#                   Metadata={
#                       'x-amz-meta-my-key': 'your-value'
#                   }
#                 )

doc= load_s3_file('colton_test_transcript.txt', "coursebuddy")
print(doc)