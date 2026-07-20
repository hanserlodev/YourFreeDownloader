@echo off
REM Run script for Windows

set DESKTOP_DIR=%~dp0..
set VENV_DIR=%DESKTOP_DIR%\venv

echo Starting YourFreeDownloader...

REM Create virtual environment if not exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

REM Activate venv
call "%VENV_DIR%\Scripts\activate.bat"

REM Install/update dependencies
python -m pip install --upgrade pip >nul 2>&1
pip install -r "%DESKTOP_DIR%\requirements.txt" >nul 2>&1

REM Install shared library
pip install -e "%DESKTOP_DIR%\..\shared" >nul 2>&1

REM Run application
cd /d "%DESKTOP_DIR%"
python -m ytdlp_desktop