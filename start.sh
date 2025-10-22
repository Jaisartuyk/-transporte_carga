#!/bin/bash

# Script de inicio para Railway con Gunicorn
# Gunicorn es más estable que Daphne en Railway

echo "Starting Gunicorn with Uvicorn worker on port 8080..."

# Iniciar Gunicorn con worker de Uvicorn (soporta WebSockets)
exec gunicorn core.asgi:application \
    --bind 0.0.0.0:8080 \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
