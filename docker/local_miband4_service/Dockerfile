FROM ubuntu:20.04

COPY . /app
WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y libglib2.0-dev
RUN apt install -y python3-pip
RUN apt-get install -y bluez bluetooth
RUN pip3 install -r ./miband4/requirements.txt --no-cache-dir
RUN pip3 install -r ./miband4_api/requirements.txt --no-cache-dir

ENV TZ Japan

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
