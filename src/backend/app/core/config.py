from dotenv import load_dotenv
import os

load_dotenv()

API_V1_STR = "/api/v1"

PROJECT_NAME = os.getenv("PROJECT_NAME", "CourseBuddyAI")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")

SECRET_KEY=os.getenv("SECRET_KEY")
