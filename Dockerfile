FROM python:3.10-buster

#Install all dependencies
RUN apt update
RUN apt-get install build-essential \
                    autoconf \
                    make \
                    git -y


RUN git clone "https://git.ffmpeg.org/ffmpeg.git"
RUN autoconf ./ffmpeg/configure
RUN make ./ffmpeg/Makefile


RUN mkdir /app
ADD . /app
WORKDIR /app

#COPY bot/requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
#RUN pip3 install python-dotenv




COPY . .

ENTRYPOINT [ "python", "bot/main.py"]