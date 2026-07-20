# Compilación y distribución - Desktop

## Requisitos previos

- Python 3.8+
- Dependencias: `pip install customtkinter yt-dlp pyinstaller`
- FFmpeg (opcional pero recomendado para MP3)

## Método 1: Script automático (recomendado)

```bash
# Linux
cd desktop-multiplatform
./scripts/build-linux.sh

# Windows
cd desktop-multiplatform
scripts\build-windows.bat
```

Los scripts:
- Crean/usan entorno virtual
- Instalan dependencias
- Instalan `ytdlp-core` en modo desarrollo
- Ejecutan PyInstaller con configuración completa

## Método 2: Manual

```bash
cd desktop-multiplatform
source venv/bin/activate    # Linux
# venv\Scripts\activate     # Windows

pip install pyinstaller
pip install -e ../../shared

pyinstaller \
  --name "YourFreeDownloader" \
  --onefile \
  --windowed \
  --icon="resources/icon.ico" \
  --add-data "../../shared/ytdlp_core:ytdlp_core" \
  --collect-all ytdlp_core \
  --collect-all yt_dlp \
  --collect-all customtkinter \
  --collect-all dependency_injector \
  --hidden-import ytdlp_core \
  --hidden-import ytdlp_core.core \
  --hidden-import ytdlp_core.domain \
  --hidden-import ytdlp_core.application \
  --hidden-import ytdlp_core.infrastructure \
  --hidden-import yt_dlp \
  --hidden-import customtkinter \
  --hidden-import dependency_injector \
  src/ytdlp_desktop/__main__.py
```

## Incluir FFmpeg (Windows)

Para que el ejecutable sea standalone y convierta a MP3 sin FFmpeg en el sistema:

```
desktop-multiplatform/
├── ffmpeg/
│   └── bin/
│       ├── ffmpeg.exe      # requerido
│       └── ffprobe.exe     # opcional
├── src/
└── scripts/
```

Descarga FFmpeg "essentials" desde https://www.gyan.dev/ffmpeg/builds/ y extrae `ffmpeg.exe` y `ffprobe.exe` en `ffmpeg/bin/`.

El código detecta automáticamente FFmpeg en:
1. `ffmpeg/bin/ffmpeg.exe` (recomendado)
2. `ffmpeg/ffmpeg.exe`
3. `bin/ffmpeg.exe`
4. `ffmpeg.exe` (raíz)
5. PATH del sistema
6. Ubicaciones comunes de Windows

Verifica en logs: `✅ FFmpeg encontrado en: ...\ffmpeg\bin\ffmpeg.exe`

## Output

Ejecutable en `desktop-multiplatform/dist/YourFreeDownloader` (Linux) o `YourFreeDownloader.exe` (Windows).

Tamaño típico:
- Sin FFmpeg: ~40-50 MB
- Con FFmpeg: ~60-80 MB

## Distribución

Solo necesitas distribuir el ejecutable. Al ejecutarse crea automáticamente carpeta `YouTubeDownloader_Data` junto al exe con:
- `config.json` - configuración persistente
- `descargador.log` - historial de actividad

No se pierde configuración entre ejecuciones.

## Archivos que NO distribuir

- Código fuente (`src/`, `*.py`)
- Scripts de build (`scripts/`, `*.bat`, `*.sh`)
- Archivos `.spec`
- Carpetas `build/`, `__pycache__/`, `venv/`

## Troubleshooting build

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError: customtkinter` | `pip install customtkinter` en venv |
| Ejecutable muy grande | Normal. Usa FFmpeg "essentials" (~70 MB). UPX ya activado en .spec |
| Error al ejecutar .exe | Verifica permisos escritura en carpeta. Antivirus puede bloquear. |
| Carpeta _Data no se crea | El .exe necesita permisos escritura en su directorio |
| `No module named 'pathlib'` | Python muy antiguo. `pip install pathlib` |

## Notas de licencia

- FFmpeg es software libre (GPL/LGPL). Puedes distribuirlo con tu app.
- No requiere licencia comercial para uso personal.
- El .exe resultante es solo para Windows. Para Linux/Mac necesitas builds separados.