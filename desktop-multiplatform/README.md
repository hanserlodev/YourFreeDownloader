# YourFreeDownloader - Desktop

Aplicación de escritorio para descargar video y audio de YouTube. Windows y Linux.

## Características

- Interfaz CustomTkinter con tema oscuro/claro
- Descarga video (múltiples calidades MP4) y audio (MP3)
- Progreso en tiempo real: velocidad, ETA, bytes descargados
- Configuración persistente (JSON)
- Detección automática de FFmpeg (incluido en ejecutable Windows)
- Descargas concurrentes (3 workers)

## Requisitos

**Sistema**
- Python 3.8+
- Tk/Tkinter
  - Arch: `sudo pacman -S tk`
  - Ubuntu/Debian: `sudo apt install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
- FFmpeg (opcional, para MP3 y merge HQ)
  - Arch: `sudo pacman -S ffmpeg`
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - Fedora: `sudo dnf install ffmpeg`

**Python** (se instalan automáticamente)
- customtkinter
- yt-dlp
- pyinstaller (para compilar)

## Instalación

### Opción 1: Scripts automáticos (recomendado)

Manejan entorno virtual y dependencias.

```bash
# Desde raíz del proyecto
./start.sh

# O desde desktop-multiplatform
cd desktop-multiplatform
./scripts/run-linux.sh        # Linux
scripts\run-windows.bat       # Windows
```

> **Linux moderno (Arch, Ubuntu 23.04+, Debian 12+)**: No uses `pip install` global. Los scripts crean venv automáticamente (PEP 668).

### Opción 2: Manual

```bash
cd desktop-multiplatform
python3 -m venv venv
source venv/bin/activate      # Linux
# venv\Scripts\activate       # Windows
pip install -r requirements.txt
python src/yt-downlader.py
```

### Opción 3: Compilar ejecutable

```bash
# Linux
cd desktop-multiplatform/scripts
./build-linux.sh

# Windows
cd desktop-multiplatform\scripts
build-windows.bat
```

Ejecutable en `desktop-multiplatform/dist/YourFreeDownloader`

## Uso

1. Ejecuta la app
2. Pega URL de YouTube
3. Selecciona formato: video (calidad) o audio (MP3)
4. Elige carpeta destino (opcional)
5. Descargar

## Estructura

```
desktop-multiplatform/
├── src/ytdlp_desktop/     # Código refactorizado (Clean Architecture)
│   ├── __main__.py        # Entry point
│   ├── config/            # AppConfig, ConfigManager
│   ├── data/services.py   # DI Container
│   ├── di/container.py    # dependency-injector wiring
│   ├── domain/models.py   # AppConfig, DownloadTask, VideoInfoDisplay
│   ├── platform/          # DesktopPlatformService
│   ├── ui/main_window.py  # CustomTkinter UI
│   └── utils/logger.py
├── scripts/               # build/run scripts
├── pyproject.toml         # Build config + deps
├── requirements.txt
└── tests/
```

## Troubleshooting Linux

Ver [TROUBLESHOOTING_LINUX.md](TROUBLESHOOTING_LINUX.md) para detalles.

Errores comunes:

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError: customtkinter` | Usa `./scripts/run-linux.sh` (crea venv) |
| `externally-managed-environment` | No uses pip global. Usa los scripts o venv manual |
| `libtk8.6.so not found` | Instala tk: `sudo pacman -S tk` / `sudo apt install python3-tk` |
| `No module named venv` | `sudo apt install python3-venv` / `sudo dnf install python3-virtualenv` |
| FFmpeg not found | `sudo pacman -S ffmpeg` / `sudo apt install ffmpeg` |

## Tests y lint

```bash
cd desktop-multiplatform
pip install -e ../shared[dev]
pip install pytest pytest-qt ruff black mypy
ruff check src/
black --check src/
mypy src/
pytest -v
```

## Licencia

MIT