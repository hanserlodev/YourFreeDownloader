@echo off
REM ========================================
REM Compilacion Rapida - PyInstaller
REM YouTube Downloader v2.0
REM ========================================

echo.
echo ==========================================
echo   COMPILACION RAPIDA - PyInstaller
echo ==========================================
echo.
echo Este script compilara el ejecutable usando
echo el archivo .spec existente (mas rapido)
echo.

REM Limpiar builds anteriores
echo [1/3] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Compilar
echo [2/3] Compilando con yt-downlader.spec...
pyinstaller yt-downlader.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Fallo la compilacion
    echo.
    echo Intenta ejecutar compilar.bat en su lugar
    pause
    exit /b 1
)

echo.
echo [3/3] Verificando ejecutable...

if exist "dist\YouTubeDownloader.exe" (
    echo.
    echo ==========================================
    echo   COMPILACION EXITOSA!
    echo ==========================================
    echo.
    echo Ejecutable: dist\YouTubeDownloader.exe
    echo.
    for %%A in ("dist\YouTubeDownloader.exe") do (
        set size=%%~zA
        set /a sizeMB=!size! / 1048576
        echo Tamano: !sizeMB! MB
    )
    echo.
    echo ==========================================
    echo.
    
    explorer dist
) else (
    echo.
    echo [ERROR] No se encontro el ejecutable
    pause
    exit /b 1
)

pause
