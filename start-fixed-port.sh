#!/bin/bash

# Script de inicio con puerto fijo para Railway
# Usar si la variable PORT no funciona

echo "Starting Daphne server on port 8000..."

# Iniciar Daphne en puerto 8000
exec daphne -b 0.0.0.0 -p 8000 core.asgi:application
