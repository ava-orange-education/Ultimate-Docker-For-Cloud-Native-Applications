FROM python:3.11-alpine AS base

WORKDIR /app

COPY requirements.txt /

RUN pip install -r /requirements.txt -U pip

COPY *.py Procfile ./

CMD ["honcho", "start"]
