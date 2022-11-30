FROM anibali/pytorch:1.11.0-nocuda-ubuntu20.04

USER root
RUN mkdir -p /demo
WORKDIR /demo

COPY . /demo

#RUN apk add --update gcc gfortran musl-dev

RUN python3 -m venv ./venv

RUN source ./venv/bin/activate
RUN pip install -r requirements.txt


EXPOSE 5000 8765
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]