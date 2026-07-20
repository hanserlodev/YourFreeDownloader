# Arquitectura de YourFreeDownloader

## Visión general

YourFreeDownloader separa la lógica de negocio compartida (`ytdlp-core`) de las implementaciones específicas por plataforma (Desktop, Android). Ambas apps dependen únicamente de las abstracciones del dominio, no de implementaciones concretas.

## Diagrama

```
┌─────────────────────────────────────────────────────────────┐
│                    YourFreeDownloader                        │
├──────────────────┬──────────────────┬────────────────────────┤
│   Desktop App    │   Android App    │     Shared Core        │
│ (Python/CustomTK)│  (Kotlin/Compose)│      (ytdlp-core)      │
├──────────────────┼──────────────────┼────────────────────────┤
│ Presentation     │ Presentation     │ Domain                 │
│ - MainWindow     │ - DownloadScreen │ - Models               │
│ - Components     │ - ViewModel      │ - Ports (interfaces)   │
├──────────────────┼──────────────────├────────────────────────┤
│ Data             │ Data             │ Application            │
│ - ConfigStore    │ - Python Bridge  │ - Use Cases            │
│ - PlatformService│ - Permissions    │                        │
├──────────────────┼──────────────────├────────────────────────┤
│                  │                  │ Infrastructure         │
│                  │                  │ - yt-dlp impl          │
│                  │                  │ - FFmpeg locator       │
│                  │                  │ - Config/Cache stores  │
└──────────────────┴──────────────────┴────────────────────────┘
```

## Principios

1. **Inversión de dependencias**: Las apps usan puertos (interfaces), las implementaciones se inyectan
2. **Responsabilidad única**: Cada módulo tiene una razón para cambiar
3. **Testabilidad**: El core es agnóstico a plataforma y se prueba con mocks
4. **Separación de responsabilidades**: UI, lógica de negocio e infraestructura aisladas

## ytdlp-core (shared)

### Dominio (`domain/`)

- **Modelos**: `VideoInfo`, `VideoFormat`, `DownloadOptions`, `DownloadProgress`, `DownloadResult`, `MediaType`
- **Puertos**: `IVideoInfoExtractor`, `IDownloader`, `IFFmpegLocator`, `IConfigStore`, `ICacheStore`, `IPlatformService`
- **Excepciones**: `ExtractionError`, `DownloadError`, `FFmpegError`, `ValidationError`

### Aplicación (`application/`)

- `GetVideoInfoUseCase`: Obtiene metadata y formatos, con caché
- `DownloadVideoUseCase`: Orquesta descarga con progreso y FFmpeg
- `GetDefaultOptionsUseCase` / `SaveDefaultOptionsUseCase`: Configuración

### Infraestructura (`infrastructure/`)

- `YtDlpVideoInfoExtractor` / `YtDlpDownloader`: Implementaciones con yt-dlp
- `FFmpegLocator`: Busca ffmpeg (bundled, PATH, ubicaciones comunes)
- `JsonConfigStore` / `MemoryCacheStore`: Persistencia
- `DesktopPlatformService`: Directorio de datos, descargas, notificaciones

## Desktop App (`desktop-multiplatform/src/ytdlp_desktop/`)

```
ytdlp_desktop/
├── __main__.py              # Entry point
├── config/manager.py        # AppConfig + ConfigManager
├── data/services.py         # DesktopServiceContainer (DI)
├── di/container.py          # dependency-injector wiring
├── domain/models.py         # AppConfig, DownloadTask, VideoInfoDisplay
├── platform/desktop_platform.py  # IPlatformService impl
├── ui/main_window.py        # CustomTkinter UI
└── utils/logger.py
```

**Flujo**: MainWindow → Use Cases (via container) → ytdlp-core → yt-dlp/FFmpeg

## Android App (`mobile-android/`)

```
youfreedownlader/
├── MainActivity.kt              # Compose entry
├── YourFreeDownloaderApplication.kt  # Inicializa Chaquopy
├── domain/model/DownloadModels.kt   # VideoInfo, VideoFormat, DownloadProgress
├── ui/
│   ├── screen/DownloadScreen.kt     # Compose UI (Material3)
│   ├── viewmodel/DownloadViewModel.kt  # State + Python bridge
│   └── theme/                       # Material3 theme
└── python/hanserlod.py              # Chaquopy module
```

**Flujo**: DownloadScreen → DownloadViewModel → Python bridge (hanserlod.py) → yt-dlp/FFmpeg

### Android-specific

- **Scoped Storage**: MediaStore (API 29+), directorio Downloads público (legacy)
- **Foreground Service**: Descargas en background con notificación
- **Intent filters**: Maneja `youtube.com/watch`, `youtu.be`, `youtube.com/shorts`
- **Lifecycle**: ViewModel sobrevive a rotación, corrutinas en `viewModelScope`

## Build

| Plataforma | Herramienta | Output |
|------------|-------------|--------|
| Desktop | PyInstaller | `YourFreeDownloader` (Linux), `YourFreeDownloader.exe` (Windows) |
| Android | Gradle + Chaquopy | `app-debug.apk`, `app-release.aab` |

Scripts en `desktop-multiplatform/scripts/` manejan venv y dependencias automáticamente.

## CI/CD

`.github/workflows/ci-cd.yml`:

1. **Shared**: lint (ruff/black/mypy) + pytest
2. **Desktop**: lint + pytest-qt + PyInstaller build
3. **Android**: `assembleDebug` + `bundleRelease` + unit tests
4. **Release** (en tag): Une artifacts y crea GitHub Release

## Flujo de dependencias

```
Desktop App     Android App
      │               │
      ▼               ▼
┌─────────────────────────────┐
│      ytdlp-core             │
│  ┌─────────────────────┐    │
│  │ Domain (models,     │    │
│  │  ports, exceptions) │    │
│  │ Application (UCs)   │    │
│  └─────────────────────┘    │
│  ┌─────────────────────┐    │
│  │ Infrastructure      │    │
│  │ (impls inyectadas)  │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

Las apps solo importan `domain` y `application`. `infrastructure` se inyecta en runtime.

## Próximos pasos

- Kotlin Multiplatform para compartir `domain` entre Desktop (Compose Desktop) y Android
- Plugin architecture para otras plataformas de video
- Cola de descargas persistente con reintentos
- Sincronización de configuración opcional
- Soporte macOS en CI