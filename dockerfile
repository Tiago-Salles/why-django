FROM python:3.13-slim

WORKDIR /app

COPY ./catalog_ops /app

RUN apt-get -y update && apt-get install -y make

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sleep", "infinity"]