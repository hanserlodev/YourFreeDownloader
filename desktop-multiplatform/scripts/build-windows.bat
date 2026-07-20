@echo off
REM Build script for Windows

set PROJECT_ROOT=%~dp0..\..
set DESKTOP_DIR=%PROJECT_ROOT%\desktop-multiplatform
set BUILD_DIR=%DESKTOP_DIR%\build
set DIST_DIR=%DESKTOP_DIR%\dist

echo Building YourFreeDownloader for Windows...

REM Clean previous builds
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"

REM Create virtual environment if not exists
if not exist "%DESKTOP_DIR%\venv" (
    echo Creating virtual environment...
    python -m venv "%DESKTOP_DIR%\venv"
)

REM Activate venv and install dependencies
call "%DESKTOP_DIR%\venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r "%DESKTOP_DIR%\requirements.txt"
pip install pyinstaller

REM Install shared library in development mode
pip install -e "%PROJECT_ROOT%\shared"

REM Run PyInstaller
cd /d "%DESKTOP_DIR%"
pyinstaller ^
    --name "YourFreeDownloader" ^
    --onefile ^
    --windowed ^
    --add-data "%PROJECT_ROOT%\shared\ytdlp_core;ytdlp_core" ^
    --collect-all ytdlp_core ^
    --collect-all yt_dlp ^
    --collect-all customtkinter ^
    --collect-all dependency_injector ^
    --hidden-import ytdlp_core ^
    --hidden-import ytdlp_core.core ^
    --hidden-import ytdlp_core.domain ^
    --hidden-import ytdlp_core.application ^
    --hidden-import ytdlp_core.infrastructure ^
    --hidden-import yt_dlp ^
    --hidden-import customtkinter ^
    --hidden-import dependency_injector ^
    src\ytdlp_desktop\__main__.py

echo Build complete! Executable at: %DIST_DIR%\YourFreeDownloader.exe