#!/bin/sh

echo "Waiting for postgres ..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
  done

  echo "PostgreSQL started"

python manage.py makemigrations
python manage.py migrate


# Start the application
echo "Starting application..."
exec "$@"

