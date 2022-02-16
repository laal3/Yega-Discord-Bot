FROM python:3.10-buster

WORKDIR /usr/app/src

COPY bot/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "main.py"]