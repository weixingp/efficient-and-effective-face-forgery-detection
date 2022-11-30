FROM anibali/pytorch:1.11.0-nocuda-ubuntu20.04
RUN mkdir /app
WORKDIR /app

COPY . /app

#RUN apk add --update gcc gfortran musl-dev

RUN pip install -r requirements.txt


EXPOSE 5000 8765
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]