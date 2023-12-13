**File Upload Service**

The FIle Upload Service takes the uploaded lecture transcripts & slides then persists them to a DigitalOcean Spaces bucket compatible with the AWS S3 API. 
This allows for the retrieval of the stored documents by the Document Embedding & Summarization Services.
It also provides a endpoint for the frontend to get a list of uploaded documents to display to the user. When clicked on the filename, it will fetch the summary generated for that document. 

Endpoints:

*Upload Lecture Transcript*

Http method - POST

url- /api/v1/file_upload/uploadTranscript

*Get Lecture Transcript*

Http method - GET

url /api/v1/file_upload/retrieveTranscript/

*Upload Lecture Slide*

Http method - POST

url /api/v1/file_upload/uploadSlide

*Upload Lecture Slides*

Http method - POST

url /api/v1/file_upload/uploadSlides

*Get Lecture Slide*

Http method - GET

url /api/v1/file_upload/retrieveSlide

*List Lecture Materials*

Http method -GET

url /api/v1/file_upload/listLectureMaterials

*Remove Course File*

Http method - DELETE

url /api/v1/file_upload/removeCourseFile
