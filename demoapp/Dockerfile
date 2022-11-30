FROM anibali/pytorch:1.11.0-nocuda-ubuntu20.04

RUN mkdir -p /demo
RUN chown weixing /demo
USER weixing
WORKDIR /newfolder

WORKDIR /demo

COPY . /demo

#RUN apk add --update gcc gfortran musl-dev

RUN pip install -r requirements.txt


EXPOSE 5000 8765
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]