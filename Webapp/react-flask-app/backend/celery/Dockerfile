FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /celery
WORKDIR /celery

ENTRYPOINT celery -A tasks worker --loglevel=info
