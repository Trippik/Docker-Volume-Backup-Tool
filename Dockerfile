FROM ubuntu:20.04

MAINTAINER Cameron Trippick "trippickc@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev


WORKDIR /

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "docker_volume_backup/app.py" ]