from celery import Celery
from app.core import config

celery_app = Celery("worker", broker=config.settings.CELERY_BROKER_URL)

celery_app.conf.task_routes = {"app.tasks.*": "main-queue"}
