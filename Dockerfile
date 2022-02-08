FROM python:3.8-buster

WORKDIR /DCBot/bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "python3", "main.py"]