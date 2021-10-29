FROM python:3.10.0-alpine
LABEL authors="45 Degrees && Caffeine Devs"

RUN pip install --upgrade pip

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

RUN adduser -D user
USER user