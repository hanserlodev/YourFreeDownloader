# YourFreeDownloader

Descargador de YouTube multiplataforma: escritorio (Windows/Linux) y Android.

## Plataformas

| Plataforma | Tech Stack | Estado |
|------------|------------|--------|
| **Desktop** | Python 3.11+, CustomTkinter, yt-dlp | ✅ Completo |
| **Android** | Kotlin, Jetpack Compose, Chaquopy (Python) | ✅ Completo |

## Inicio rápido

### Desktop (Linux)

```bash
./start.sh
```

O manualmente:

```bash
cd desktop-multiplatform
./scripts/run-linux.sh
```

### Desktop (Windows)

```cmd
cd desktop-multiplatform
scripts\run-windows.bat
```

### Android

```bash
cd mobile-android
./gradlew assembleDebug
```

O abre `mobile-android` en Android Studio.

## Características principales

**Desktop**
- Interfaz CustomTkinter con tema oscuro/claro
- Descarga video (múltiples calidades MP4) y audio (MP3)
- Progreso en tiempo real (velocidad, ETA, bytes)
- Configuración persistente (JSON)
- Detección automática de FFmpeg (incluido en ejecutable Windows)
- Descargas concurrentes (3 workers)

**Android**
- UI Material 3 con Compose
- ViewModel + StateFlow + corrutinas
- Scoped Storage (API 29+) + MediaStore
- Foreground Service para descargas en background
- Intent filters para URLs de YouTube
- Python backend via Chaquopy (yt-dlp + ffmpeg-python)

## Arquitectura

Clean Architecture con librería compartida (`shared/ytdlp-core`):

```
shared/ytdlp-core/     # Domain + Application + Infrastructure (Python)
├── domain/            # Modelos, puertos (interfaces), excepciones
├── application/       # Casos de uso
└── infrastructure/    # Implementaciones yt-dlp, FFmpeg, config, cache

desktop-multiplatform/ # App Python/CustomTkinter
mobile-android/        # App Kotlin/Compose
```

Ver [ARCHITECTURE.md](ARCHITECTURE.md) para detalles.

## Requisitos

**Desktop**
- Python 3.8+
- Tk/Tkinter (Linux: `python3-tk` / `tk` / `python3-tkinter`)
- FFmpeg opcional (para MP3 y merge HQ)

**Android**
- Android Studio
- JDK 11
- Android SDK 36
- Dispositivo/emulador API 24+

## Scripts útiles

| Comando | Descripción |
|---------|-------------|
| `./start.sh` | Inicio rápido desktop (Linux) |
| `desktop-multiplatform/scripts/build-linux.sh` | Compilar ejecutable Linux |
| `desktop-multiplatform/scripts/build-windows.bat` | Compilar ejecutable Windows |
| `mobile-android/gradlew assembleDebug` | APK debug |
| `mobile-android/gradlew bundleRelease` | AAB release |

## Documentación

- [Arquitectura](ARCHITECTURE.md) - Clean Architecture, DI, capas
- [Contribuir](CONTRIBUTING.md) - Setup, convención commits, PRs, testing
- [Desktop README](desktop-multiplatform/README.md) - Instalación, troubleshooting Linux
- [Android README](mobile-android/README.md) - Build, estructura, Chaquopy
- [Troubleshooting Linux](desktop-multiplatform/TROUBLESHOOTING_LINUX.md) - Errores comunes Linux

## Licencia

MIT - ver [LICENSE](LICENSE)

## Autor

**HanserlodXP**

## Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Motor de descarga
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - UI desktop
- [FFmpeg](https://ffmpeg.org/) - Procesamiento multimedia
- [Chaquopy](https://chaquo.com/chaquopy/) - Python en Android