@echo off
REM Script para ejecutar la aplicación en Windows

echo 🚀 Iniciando YouTube Downloader...

REM Activar entorno virtual si existe
if exist "venv\" (
    call venv\Scripts\activate.bat
)

REM Ejecutar la aplicación
python src\yt-downlader.py

REM Desactivar entorno virtual
if exist "venv\" (
    call venv\Scripts\deactivate.bat
)

pause
