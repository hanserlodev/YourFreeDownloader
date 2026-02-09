#!/bin/bash
# Script de inicio rápido - YourFreeDownloader

clear
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║         YouTube Downloader - Inicio Rápido (Linux)               ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Cambiar al directorio desktop-multiplatform
if [ ! -d "desktop-multiplatform" ]; then
    echo "❌ No se encuentra el directorio desktop-multiplatform"
    echo "   Asegúrate de ejecutar este script desde la raíz del proyecto"
    exit 1
fi

cd desktop-multiplatform

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo ""
    echo "Instálalo según tu distribución:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "  - Arch: sudo pacman -S python"
    echo "  - Fedora: sudo dnf install python3"
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"
echo ""

# Verificar si Tk/Tcinter está instalado (requerido para GUI)
echo "🔍 Verificando Tk/Tcinter..."
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo ""
    echo "❌ Tk/Tcinter no está instalado (requerido para la interfaz gráfica)"
    echo ""
    echo "📦 Instálalo según tu distribución:"
    echo ""
    if command -v pacman &> /dev/null; then
        echo "  🔹 Arch Linux:"
        echo "     sudo pacman -S tk"
    elif command -v apt &> /dev/null; then
        echo "  🔹 Ubuntu/Debian:"
        echo "     sudo apt install python3-tk"
    elif command -v dnf &> /dev/null; then
        echo "  🔹 Fedora:"
        echo "     sudo dnf install python3-tkinter"
    elif command -v zypper &> /dev/null; then
        echo "  🔹 openSUSE:"
        echo "     sudo zypper install python3-tk"
    else
        echo "  🔹 Tu distribución:"
        echo "     Busca el paquete 'tk' o 'python-tk' o 'python3-tk'"
    fi
    echo ""
    echo "Después de instalarlo, ejecuta este script nuevamente."
    exit 1
fi

echo "✅ Tk/Tcinter encontrado"
echo ""

# Verificar si existe entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Primera ejecución detectada"
    echo "   Configurando entorno virtual..."
    echo ""
    
    # Crear entorno virtual
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear entorno virtual"
        echo ""
        echo "Instala python3-venv:"
        echo "  - Ubuntu/Debian: sudo apt install python3-venv"
        echo "  - Arch: ya incluido con python"
        echo "  - Fedora: sudo dnf install python3-virtualenv"
        exit 1
    fi
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Actualizar pip
    echo "📥 Actualizando pip..."
    pip install --upgrade pip > /dev/null 2>&1
    
    # Instalar dependencias
    echo "📥 Instalando dependencias (esto tomará un momento)..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        deactivate
        exit 1
    fi
    
    echo ""
    echo "✅ Configuración completada"
else
    # Activar entorno existente
    source venv/bin/activate
    
    # Verificar dependencias
    if ! python -c "import customtkinter, yt_dlp" 2>/dev/null; then
        echo "📥 Instalando dependencias faltantes..."
        pip install -r requirements.txt
    fi
fi

# Verificar FFmpeg (opcional)
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "⚠️  FFmpeg no está instalado (opcional para conversión MP3)"
    echo "   Para instalarlo:"
    echo "   - Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   - Arch: sudo pacman -S ffmpeg"
    echo "   - Fedora: sudo dnf install ffmpeg"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                 🚀 Iniciando la aplicación...                     ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Ejecutar aplicación
python src/yt-downlader.py

# Desactivar entorno virtual al salir
deactivate

echo ""
echo "👋 Aplicación cerrada"
