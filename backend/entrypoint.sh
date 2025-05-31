#!/bin/sh

echo "Waiting for postgres ..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
  done

  echo "PostgreSQL started"

python manage.py makemigrations
echo "Running database migrations..."
python manage.py makemigrations
if [ $? -eq 0 ]; then
    echo "No migrations needed"
else
    python manage.py migrate
fi

# Start the application
echo "Starting application..."
exec "$@"

