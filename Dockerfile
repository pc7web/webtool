ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG DEBUG
ARG SECRET_KEY
ARG WEB_NAME
ARG DB_DEFAULT2
ARG ALLOWED_HOSTS
ARG CSRF_TRUSTED_ORIGINS
ARG CORS_ORIGIN
ARG DB_HOST
ARG DB_USER
ARG DB_PORT
ARG DB_NAME
ARG DB_PASS
ARG GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "web_tool.wsgi"]
