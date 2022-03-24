FROM python:3.10-buster
FROM jrottenberg/ffmpeg:latest

RUN apt-get update && apt-get install -y python3.9 python3-pip

RUN mkdir /app
ADD . /app
WORKDIR /app

COPY bot/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install python-dotenv

COPY . .

ENTRYPOINT [ "python", "bot/main.py"]