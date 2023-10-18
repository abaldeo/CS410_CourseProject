from .service import Summary

def check_cache(course_name: str, video_name: str) -> Summary:
    return Summary(courseName=course_name, videoName=video_name, summary="summary")

def get_video_transcript():
    pass

def generate_summary() -> Summary:
    return Summary(courseName=course_name, videoName=video_name, summary="summary")