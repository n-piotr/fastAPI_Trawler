FROM python:3.11.6-alpine3.18

WORKDIR /web

COPY . /web

RUN pip install --no-cache-dir --upgrade -r /web/requirements.txt

EXPOSE 8000