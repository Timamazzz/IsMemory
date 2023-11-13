FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=IsMemory.settings

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y wait-for-it

RUN pip install -r requirements.txt

COPY . /app/
