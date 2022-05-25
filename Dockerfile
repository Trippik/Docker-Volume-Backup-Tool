FROM ubuntu:20.04

MAINTAINER Cameron Trippick "trippickc@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev


COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "docker_volume_backup/app.py" ]