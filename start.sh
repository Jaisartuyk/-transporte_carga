#!/bin/bash

# Script de inicio para Railway con Daphne

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Daphne server on port $PORT..."

# Iniciar Daphne
exec daphne -b 0.0.0.0 -p $PORT core.asgi:application