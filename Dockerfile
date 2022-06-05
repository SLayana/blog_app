FROM python:alpine3.16
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps
COPY . /code/