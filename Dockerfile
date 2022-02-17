FROM python:3.10-buster

RUN mkdir /app
ADD . /app
WORKDIR /app

COPY bot/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install python-dotenv

COPY . .

ENTRYPOINT [ "python", "bot/main.py"]