web: uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
worker: celery -A main:worker beat --loglevel=info -s /tmp/celerybeat-schedule
