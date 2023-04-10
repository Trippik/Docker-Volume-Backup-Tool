FROM ubuntu:23.04

MAINTAINER Cameron Trippick "trippickc@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev


COPY ./requirements.txt /requirements.txt

COPY ./setup.py /setup.py

COPY . /

WORKDIR /

RUN pip3 install -r requirements.txt

RUN python3 setup.py install

ENV TARGET-MODE = "Placeholder"

ENV STORAGE-SERVER = "Placeholder"

ENV USERNAME = "Placeholder"

ENV PASSWORD = "Placeholder"

ENV PORT = "Placeholder"

ENV NUMBER-OF-BACKUPS = "Placeholder"

ENV REPORTING_HOUR = "Placeholder"

ENV ACCESS-KEY-ID = "Placeholder"

ENV SECRET-KEY = "Placeholder"

CMD [ "Docker-Volume-Backup-Tool" ]