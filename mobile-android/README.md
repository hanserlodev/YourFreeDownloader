# YourFreeDownloader - Android

App nativa Android para descargar video y audio de YouTube.

## Características

- UI Material 3 con Jetpack Compose
- ViewModel + StateFlow + corrutinas
- Scoped Storage (API 29+) con fallback MediaStore
- Foreground Service para descargas en background
- Intent filters para URLs de YouTube (watch, shorts, youtu.be)
- Backend Python vía Chaquopy (yt-dlp + ffmpeg-python)

## Requisitos de desarrollo

- Android Studio (Arctic Fox+)
- JDK 11
- Android SDK 36
- Gradle 8.x (incluido via wrapper)

## Build

```bash
cd mobile-android

# Debug APK
./gradlew assembleDebug

# Release AAB (para Play Store)
./gradlew bundleRelease

# Tests
./gradlew test
./gradlew connectedAndroidTest  # requiere emulador/dispositivo
```

## Estructura

```
mobile-android/
├── src/main/
│   ├── java/com/hanserlod/youfreedownlader/
│   │   ├── MainActivity.kt                    # Compose entry point
│   │   ├── YourFreeDownloaderApplication.kt   # Inicializa Chaquopy
│   │   ├── data/                              # Repositories (futuro)
│   │   ├── domain/model/DownloadModels.kt     # VideoInfo, VideoFormat, DownloadProgress, DownloadTask
│   │   ├── ui/
│   │   │   ├── screen/DownloadScreen.kt       # Compose UI completo
│   │   │   ├── viewmodel/DownloadViewModel.kt # Estado + Python bridge
│   │   │   └── theme/                         # Material3 Theme + Typography
│   │   └── util/
│   ├── python/hanserlod.py                    # Chaquopy bridge (yt-dlp)
│   └── res/                                   # Resources
├── build.gradle.kts                           # Compose + Chaquopy config
├── gradle/libs.versions.toml                  # Version catalog
├── gradlew / settings.gradle.kts              # Standalone Gradle project
└── proguard-rules.pro
```

## Permisos y almacenamiento

| API | Permiso | Uso |
|-----|---------|-----|
| Todas | `INTERNET` | Descargas yt-dlp |
| 29-32 | `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` | `maxSdkVersion=28`/`32` |
| 33+ | `READ_MEDIA_VIDEO` / `READ_MEDIA_AUDIO` | MediaStore acceso |
| Todas | `FOREGROUND_SERVICE` + `FOREGROUND_SERVICE_DATA_SYNC` | Background downloads |

La app usa `Environment.getExternalStoragePublicDirectory(DIRECTORY_DOWNLOADS)` para API < 29 y MediaStore para API 29+. No requiere permisos de almacenamiento en runtime en Android 11+ gracias a Scoped Storage.

## Python Bridge (Chaquopy)

`src/main/python/hanserlod.py` expone:

```python
def obtener_formatos(url) -> List[Tuple[format_id, description]]:
    # Retorna lista de (itag, "itag - 720p - mp4 (25MB)")

def descargar_video(url, output_path, format_id, solo_audio=False):
    # Descarga con progress_hook
```

## Configuración Gradle

`build.gradle.kts` incluye:
- Compose BOM 2024.08.00
- Kotlin 2.0.0 + Compose compiler 1.5.11
- Chaquopy 16.1.0 con Python 3.11
- yt-dlp + ffmpeg-python como dependencias pip
- ViewModel Compose, Navigation, Coil, Coroutines

## ProGuard/R8

`proguard-rules.pro` mantiene:
- Clases Chaquopy (`com.chaquo.python.**`)
- yt-dlp, ffmpeg-python
- App classes (`com.hanserlod.youfreedownlader.**`)
- Kotlin coroutines, Compose runtime, Lifecycle, Activity Result, Coil

## Testing

```bash
# Unit tests (JUnit)
./gradlew test

# Instrumented tests (requiere emulador/dispositivo)
./gradlew connectedAndroidTest
```

## Licencia

MIT