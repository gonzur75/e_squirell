#!/bin/bash

echo "Waiting for postgres ..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
  done

  echo "PostgreSQL started"


python manage.py makemigrations
python manage.py migrate
python uvicorn --host 0.0.0.0 --port 8000 config.asgi:application


exec "$@"