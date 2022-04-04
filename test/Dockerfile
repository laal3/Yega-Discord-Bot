FROM ubuntu:latest
FROM jrottenberg/ffmpeg:5.0-ubuntu

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN mkdir /app
ADD . /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install python-dotenv

COPY . .

ENTRYPOINT [ "python", "test2.py"]