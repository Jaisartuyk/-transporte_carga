#!/bin/bash

# Script de inicio para Railway
# Maneja la variable PORT correctamente

# Obtener el puerto de Railway o usar 8000 por defecto
PORT=${PORT:-8000}

echo "Starting Daphne server on port $PORT..."

# Iniciar Daphne
exec daphne -b 0.0.0.0 -p $PORT core.asgi:application
