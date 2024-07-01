FROM python:3.8.10-slim-buster

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirments.txt

ENTRYPOINT python server.py