FROM python:latest

MAINTAINER Cameron Trippick "trippickc@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev


COPY ./requirements.txt /requirements.txt

COPY ./setup.py /setup.py

COPY . /

WORKDIR /

RUN pip3 install -r requirements.txt

RUN python3 setup.py install

ENV TARGET-MODES "['Placeholder','Placeholder']"

ENV SUB-DIRECTORIES "['beep/boop', 'boop/beep']"

ENV STORAGE-SERVER "Placeholder"

ENV USERNAME "Placeholder"

ENV PASSWORD "Placeholder"

ENV PORT "Placeholder"

ENV NUMBER-OF-BACKUPS "Placeholder"

ENV REPORTING_HOUR "Placeholder"

ENV ACCESS-KEY-ID "Placeholder"

ENV SECRET-KEY "Placeholder"

ENV BUCKET "Placeholder"

ENV DB-FILEPATH "/databases/volume_backup_tool.db"

ENV DB-TYPE "SQLite"

ENV DB-HOST "Placeholder"

ENV DB-PORT "0000"

ENV DB-USER "Placeholder"

ENV DB-SCHEMA "volume-backup-tool"

ENV DB-PASSWORD "Placeholder"

ENV SMB-SHARE = "Placeholder"

CMD [ "Docker-Volume-Backup-Tool" ]