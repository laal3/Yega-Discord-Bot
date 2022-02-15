FROM python:3.10-buster

WORKDIR /Yega

COPY bot/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "main.py"]