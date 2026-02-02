#!/bin/bash
# Script de compilación para Linux
# YouTube Downloader - Versión Multiplataforma

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║     YouTube Downloader - Compilación para Linux                  ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instala Python3 primero."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instala pip3 primero."
    exit 1
fi

echo "✅ Python3 y pip3 encontrados"
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
