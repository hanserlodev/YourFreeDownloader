#!/bin/bash
# Script de compilación para Linux
# YouTube Downloader - Versión Multiplataforma

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║     YouTube Downloader - Compilación para Linux                  ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")/.." || exit 1

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instala Python3 primero."
    exit 1
fi

echo "✅ Python3 encontrado"

# Verificar si Tk/Tcinter está instalado (requerido para GUI)
echo "🔍 Verificando Tk/Tcinter..."
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo ""
    echo "❌ Tk/Tcinter no está instalado (requerido para la interfaz gráfica)"
    echo ""
    echo "📦 Instálalo según tu distribución:"
    if command -v pacman &> /dev/null; then
        echo "   sudo pacman -S tk"
    elif command -v apt &> /dev/null; then
        echo "   sudo apt install python3-tk"
    elif command -v dnf &> /dev/null; then
        echo "   sudo dnf install python3-tkinter"
    fi
    echo ""
    exit 1
fi

echo "✅ Tk/Tcinter encontrado"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install customtkinter yt-dlp pyinstaller

# Compilar la aplicación
echo ""
echo "🔨 Compilando aplicación..."
pyinstaller --clean --noconfirm ../config/YouTubeDownloader.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║                   ✅ COMPILACIÓN EXITOSA                          ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📂 El ejecutable se encuentra en: build/dist/"
    echo "🚀 Para ejecutar: ./build/dist/YouTubeDownloader/YouTubeDownloader"
else
    echo ""
    echo "❌ Error durante la compilación"
    exit 1
fi

# Desactivar entorno virtual
deactivate
