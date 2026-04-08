#!/bin/bash
# Startup script for SAGE Django backend
# Runs migrations, seeds data, then starts the dev server

set -e

cd "$(dirname "$0")/sage_backend"

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Seeding sample meals..."
python manage.py seed_meals

echo "Starting Django development server on port ${PORT:-8080}..."
python manage.py runserver "0.0.0.0:${PORT:-8080}"
