#!/bin/bash

# Script de inicio para Railway
# Usar puerto 8080 (asignado por Railway)

echo "Starting Daphne server on port 8080..."

# Iniciar Daphne en puerto 8080
exec daphne -b 0.0.0.0 -p 8080 core.asgi:application
