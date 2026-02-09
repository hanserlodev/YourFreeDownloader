#!/bin/bash
# Script para ejecutar la aplicación en Linux

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║           YouTube Downloader - Ejecutando                         ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")/.." || exit 1

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instala Python3 primero."
    exit 1
fi

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
    else
        echo "   Busca el paquete 'tk' o 'python-tk' en tu gestor de paquetes"
    fi
    echo ""
    exit 1
fi

echo "✅ Tk/Tcinter encontrado"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Entorno virtual no encontrado. Creando..."
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual."
        echo "   Asegúrate de tener python3-venv instalado:"
        echo "   - Ubuntu/Debian: sudo apt install python3-venv"
        echo "   - Arch: python viene con venv incluido"
        echo "   - Fedora: sudo dnf install python3-virtualenv"
        exit 1
    fi
    
    echo "✅ Entorno virtual creado"
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Instalar dependencias
    echo "📥 Instalando dependencias..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias"
        deactivate
        exit 1
    fi
    
    echo "✅ Dependencias instaladas"
else
    # Activar entorno virtual existente
    source venv/bin/activate
    
    # Verificar si las dependencias están instaladas
    if ! python -c "import customtkinter" 2>/dev/null; then
        echo "📥 Instalando dependencias faltantes..."
        pip install --upgrade pip > /dev/null 2>&1
        pip install -r requirements.txt
    fi
fi

echo ""
echo "🚀 Iniciando YouTube Downloader..."
echo ""

# Ejecutar la aplicación
python src/yt-downlader.py

# Desactivar entorno virtual
deactivate
