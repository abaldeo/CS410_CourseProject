Summarization Service

Endpoints:

* Fetch Summary
    - Http method - Get
    - url /fetchSummary
    - params 'courseName': str and 'videoName': str
    - Response:
        Example of succes:
        {
            "courseName": "cs410", 
            "videoName": "lecture_1", 
            "summary": "Summary about lecture 1"
            "status": True,
            "msg": "Success"
        }
        Does not find summary or error:
        {
            "status": False,
            "msg": "Not Found"
        }

* Generate Summary
    - Http method - Post
    - url /fetchSummary
    - params userId: int, courseName: str, videoName: str, transcript: str
    - Response:
        succesfully finds summary:
        {
            "userId": 0
            "courseName": "cs410", 
            "videoName": "lecture_1", 
            "summary": "summary about lecture_1"
            "status": True,
            "msg": "Success"
        }
        Does not find summary or error:
        {
            "status": False,
            "msg": "Not Found"
        }
