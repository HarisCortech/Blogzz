
FROM python:3.11.7

ENV PYTHONUNBUFFERED 1 # This is to prevent Python from buffering stdout and stderr. It will print to the console immediately.
ENV PYTHONDONTWRITEBYTECODE 1 # This is to prevent Python from writing pyc files to disc (Python compiled files)


RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc

WORKDIR /app

COPY . /app/

COPY ./start.sh .
COPY  ./requirements.txt .
RUN pip install --upgrade pip setuptools && pip install --no-cache-dir -r requirements.txt

