#!/bin/bash
# Script de instalación rápida para Linux

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   YourFreeDownloader - Instalación Rápida (Linux)                ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Instalar FFmpeg si no está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "📦 FFmpeg no encontrado. Instalando..."
    
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y ffmpeg
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y ffmpeg
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm ffmpeg
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y ffmpeg
    else
        echo "⚠️  No se pudo instalar FFmpeg automáticamente."
        echo "   Por favor, instálalo manualmente según tu distribución."
    fi
else
    echo "✅ FFmpeg ya está instalado"
fi

# Entrar al directorio
cd desktop-multiplatform

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                   ✅ INSTALACIÓN COMPLETA                         ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Para ejecutar la aplicación:"
echo "  ./scripts/run-linux.sh"
echo ""
echo "Para compilar un ejecutable:"
echo "  ./scripts/build-linux.sh"
echo ""

deactivate
