@echo off
REM ========================================
REM Script de Compilacion para PyInstaller
REM Descargador de YouTube v2.0
REM ========================================

echo.
echo ========================================
echo   YouTube Downloader - Compilador
echo ========================================
echo.

REM Verificar que Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    pause
    exit /b 1
)

echo [1/5] Verificando Python... OK
echo.

REM Instalar dependencias
echo [2/5] Instalando dependencias...
pip install customtkinter yt-dlp pyinstaller
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de dependencias
    pause
    exit /b 1
)
echo.

REM Limpiar builds anteriores
echo [3/5] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo.

REM Compilar con PyInstaller
echo [4/5] Compilando aplicacion...
echo Esto puede tardar varios minutos...
echo.

pyinstaller --onefile ^
  --windowed ^
  --name "YouTubeDownloader" ^
  --hidden-import customtkinter ^
  --hidden-import yt_dlp ^
  --hidden-import PIL._tkinter_finder ^
  --exclude-module matplotlib ^
  --exclude-module pandas ^
  --exclude-module numpy ^
  yt-downlader.py

if errorlevel 1 (
    echo.
    echo [ERROR] Fallo la compilacion
    pause
    exit /b 1
)

echo.
echo [5/5] Verificando ejecutable...

if exist "dist\YouTubeDownloader.exe" (
    echo.
    echo ========================================
    echo   COMPILACION EXITOSA!
    echo ========================================
    echo.
    echo Ejecutable generado en: dist\YouTubeDownloader.exe
    echo.
    
    REM Obtener tamano del archivo
    for %%A in ("dist\YouTubeDownloader.exe") do (
        set size=%%~zA
        set /a sizeMB=!size! / 1048576
        echo Tamano: !sizeMB! MB
    )
    
    echo.
    echo IMPORTANTE:
    echo - El ejecutable creara una carpeta "YouTubeDownloader_Data"
    echo   junto al .exe para guardar:
    echo   * config.json (configuracion)
    echo   * descargador.log (registro de actividad)
    echo.
    echo - ffmpeg debe estar instalado en el sistema para
    echo   conversiones de audio (MP3) y merge de video+audio
    echo.
    echo Puedes distribuir el archivo YouTubeDownloader.exe
    echo sin necesidad de instalar Python.
    echo.
    
    REM Preguntar si abrir la carpeta
    choice /C SN /M "Abrir carpeta dist"
    if errorlevel 2 goto end
    if errorlevel 1 explorer dist
    
) else (
    echo.
    echo [ERROR] No se encontro el ejecutable generado
    pause
    exit /b 1
)

:end
echo.
echo Presiona cualquier tecla para salir...
pause >nul
