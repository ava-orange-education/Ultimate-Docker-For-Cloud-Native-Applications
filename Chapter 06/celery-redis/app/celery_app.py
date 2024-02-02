import os

from celery import Celery

REDIS_BROKER_URL = os.environ.get("REDIS_BROKER_URL", "redis://localhost:6379/0")
REDIS_BACKEND_URL = os.environ.get("REDIS_BACKEND_URL")

app = Celery(__name__, broker=REDIS_BROKER_URL, backend=REDIS_BACKEND_URL)
