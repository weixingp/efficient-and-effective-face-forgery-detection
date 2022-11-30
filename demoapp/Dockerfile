FROM anibali/pytorch:1.11.0-nocuda-ubuntu20.04

USER root
RUN mkdir -p /demo
WORKDIR /demo

COPY . /demo

#RUN apk add --update gcc gfortran musl-dev

RUN apt-get update

## for apt to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

## preesed tzdata, update package index, upgrade packages and install needed software
RUN echo "tzdata tzdata/Areas select Europe" > /tmp/preseed.txt; \
    echo "tzdata tzdata/Zones/Europe select Berlin" >> /tmp/preseed.txt; \
    debconf-set-selections /tmp/preseed.txt && \
    apt-get update && \
    apt-get install -y tzdata \

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN python3 -m venv ./venv

RUN . ./venv/bin/activate
RUN pip install -r requirements.txt


EXPOSE 5000 8765
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]