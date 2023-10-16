from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

celery_app = Celery("worker", broker=CELERY_BROKER_URL)

celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
