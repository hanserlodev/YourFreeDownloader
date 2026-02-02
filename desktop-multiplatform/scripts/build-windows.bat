@echo off
REM Script de compilación para Windows
REM YouTube Downloader - Versión Multiplataforma

echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║     YouTube Downloader - Compilación para Windows                ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor instala Python primero.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Crear entorno virtual si no existe
if not exist "venv\" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    echo ✅ Entorno virtual creado
) else (
    echo ✅ Entorno virtual ya existe
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📥 Instalando dependencias...
python -m pip install --upgrade pip
pip install customtkinter yt-dlp pyinstaller

REM Compilar la aplicación
echo.
echo 🔨 Compilando aplicación...
pyinstaller --clean --noconfirm ..\config\YouTubeDownloader.spec

if %errorlevel% equ 0 (
    echo.
    echo ╔═══════════════════════════════════════════════════════════════════╗
    echo ║                   ✅ COMPILACIÓN EXITOSA                          ║
    echo ╚═══════════════════════════════════════════════════════════════════╝
    echo.
    echo 📂 El ejecutable se encuentra en: build\dist\
    echo 🚀 Para ejecutar: build\dist\YouTubeDownloader\YouTubeDownloader.exe
) else (
    echo.
    echo ❌ Error durante la compilación
    pause
    exit /b 1
)

REM Desactivar entorno virtual
call venv\Scripts\deactivate.bat

pause
