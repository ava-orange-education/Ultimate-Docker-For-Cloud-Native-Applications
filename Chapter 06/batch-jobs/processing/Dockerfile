FROM python:3.11-alpine

WORKDIR /app

ADD requirements.txt /

RUN pip install -U pip -r /requirements.txt && \
    rm -rf /root/.cache/pip /requirements.txt

COPY *.py ./

CMD ["python", "main.py"]
