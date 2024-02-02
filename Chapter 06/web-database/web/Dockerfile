FROM python:3.11-alpine

WORKDIR /app

RUN pip install -U pip 'fastapi<1' 'uvicorn<1' 'pydantic<3' 'psycopg2-binary<3'

COPY main.py .

CMD [ "sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}" ]
