FROM python:3.10.8-alpine3.17
RUN mkdir /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt


EXPOSE 5000 8765
RUN chmod +x ./start.sh

ENTRYPOINT ["./start.sh"]