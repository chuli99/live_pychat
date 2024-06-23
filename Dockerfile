FROM python:3.8.10-alpine3.11

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirments.txt

ENTRYPOINT python server.py