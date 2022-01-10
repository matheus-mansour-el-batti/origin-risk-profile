FROM python:3.9.6-slim-buster
ENV PYTHONBUFFERED 1
ENV PYTHONPATH /app/src

WORKDIR /app
ADD requirements.txt /app/


RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app

ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

EXPOSE 8080

COPY . /app
