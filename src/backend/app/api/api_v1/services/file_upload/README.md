**File Upload Service**

The FIle Upload Service takes the uploaded lecture transcripts & slides then persists them to a DigitalOcean Spaces bucket compatible with the AWS S3 API. 
This allows for the retrieval of the stored documents by the Document Embedding & Summarization Services.
It also provides a endpoint for the frontend to get a list of uploaded documents to display to the user. When clicked on the filename, it will fetch the summary generated for that document. 

Endpoints:

*Upload Lecture Transcript*
- Http method - POST
- url - /api/v1/file_upload/uploadTranscript
- params - {userName: str, courseName: str, videoName: str, transcriptText: str}

*Get Lecture Transcript*
- Http method - GET
- url /api/v1/file_upload/retrieveTranscript/
- params - userName: str, courseName: str, videoName: str


*Upload Lecture Slide*
- Http method - POST
- url /api/v1/file_upload/uploadSlide
- params - {userName: str, courseName: str, videoName: str, slideFile: UploadFile}


*Upload Lecture Slides*
- Http method - POST
- url /api/v1/file_upload/uploadSlides
- params - {userName: str, courseName: str, slideFiles: List[UploadFile]}

*Get Lecture Slide*
- Http method - GET
- url /api/v1/file_upload/retrieveSlide
- params - userName: str, courseName: str, slideFileName : str

*List Lecture Materials*
- Http method - GET
- url /api/v1/file_upload/listLectureMaterials
- params -  courseName: str, file_type: str ["slides"|"transcripts"], userName : str


*Remove Course File*
- Http method - DELETE
- url /api/v1/file_upload/removeCourseFile
- params - userName: str, courseName: str, fileName : str
