FROM python:3.11-alpine

WORKDIR /app

RUN pip install "fastapi<1" "uvicorn<1"

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
