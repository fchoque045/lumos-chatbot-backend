FROM python:3.10.8-alpine3.15

ENV PYTHONUNBUFFERED 1 
ENV PYTHONDONTWRITEBYTECODE=1

# RUN apt-get update \
#     && apt-get install libxml2-dev libxslt-dev \
#     && apt-get install postgresql-dev gcc python3-dev musl-dev

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . /app/