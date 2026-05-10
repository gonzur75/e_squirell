#!/bin/sh
set -e

echo "Applying database migrations..."
python3 manage.py migrate

# Start the application
echo "Starting application..."
exec "$@"

