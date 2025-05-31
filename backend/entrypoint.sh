#!/bin/sh

echo "Waiting for postgres ..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
  done

  echo "PostgreSQL started"

python manage.py makemigrations
echo "Running database migrations..."
if ! python manage.py migrate --check # Check if there are unapplied migrations
then
    echo "No migrations needed"
else
    python manage.py migrate
fi

# Start the application
echo "Starting application..."
exec "$@"

