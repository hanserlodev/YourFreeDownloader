#!/bin/bash
# Script para ejecutar la aplicación en Linux

echo "🚀 Iniciando YouTube Downloader..."

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar la aplicación
python3 src/yt-downlader.py

# Desactivar entorno virtual
if [ -d "venv" ]; then
    deactivate
fi
