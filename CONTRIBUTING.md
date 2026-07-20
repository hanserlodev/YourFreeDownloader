# Contribuir a YourFreeDownloader

Gracias por tu interés en contribuir. Esta guía cubre el setup, convenciones y proceso.

## Setup de desarrollo

### Requisitos

- Python 3.11+ (desktop + shared)
- JDK 11 (Android)
- Android Studio (desarrollo Android)
- Git

### Clonar y configurar

```bash
git clone https://github.com/hanserlodev/YourFreeDownloader.git
cd YourFreeDownloader
```

### Shared library

```bash
cd shared
pip install -e .[dev]
pytest
ruff check ytdlp_core
black --check ytdlp_core
mypy ytdlp_core
```

### Desktop

```bash
cd desktop-multiplatform
# Linux
./scripts/run-linux.sh
# Windows
scripts\run-windows.bat
```

### Android

Abre `mobile-android` en Android Studio y sincroniza Gradle.

## Convenciones de código

### Python (Shared + Desktop)

- Formatter: `black` (line-length 100)
- Linter: `ruff` (con auto-fix)
- Types: `mypy`
- Tests: `pytest`

```bash
ruff check --fix .
black .
mypy .
pytest
```

### Kotlin (Android)

- Formatter: `ktlint` (via `spotless`)
- Linter: `detekt`

```bash
cd mobile-android
./gradlew spotlessApply
./gradlew detekt
```

## Arquitectura

Sigue la Clean Architecture en `shared/ytdlp_core`:

```
domain/          # Python/Kotlin puro - sin deps externas
  models/        # Entidades, value objects
  ports/         # Interfaces (IVideoInfoExtractor, IDownloader, etc.)
  exceptions/    # Excepciones de dominio
application/     # Casos de uso (GetVideoInfoUseCase, DownloadVideoUseCase)
infrastructure/  # Implementaciones (YtDlpDownloader, FFmpegLocator, etc.)
```

### Regla de dependencias

- Capas internas no conocen las externas
- Las dependencias apuntan hacia adentro
- Usa inyección de dependencias (constructor injection)

### Código específico de plataforma

- Desktop: `desktop-multiplatform/src/ytdlp_desktop/platform/`
- Android: `mobile-android/src/main/java/.../platform/`
- Ambos implementan `IPlatformService` del dominio compartido

## Convención de commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[alcance opcional]: <descripción>

[cuerpo opcional]

[footer(s) opcional]
```

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Solo documentación
- `style`: Formato, punto y coma, etc.
- `refactor`: Cambio que no corrige bug ni añade feature
- `perf`: Mejora de rendimiento
- `test`: Tests
- `chore`: Mantenimiento

Ejemplos:
```
feat(desktop): añadir toggle tema oscuro/claro
fix(android): manejar scoped storage en API 33+
docs: actualizar ARCHITECTURE.md con nuevo contenedor DI
refactor(shared): extraer interfaz FFmpegLocator
```

## Pull Requests

1. Fork del repo
2. Crea rama: `git checkout -b feat/amazing-feature`
3. Commits siguiendo la convención
4. Push: `git push origin feat/amazing-feature`
5. Abre PR contra `main`

### Requisitos del PR

- [ ] CI pasa (lint, types, tests)
- [ ] Código sigue las guías de estilo
- [ ] Tests añadidos/actualizados para nueva funcionalidad
- [ ] Documentación actualizada si aplica
- [ ] Sin breaking changes sin discusión previa
- [ ] Descripción clara del cambio

## Testing

### Shared

```bash
cd shared
pytest -v --cov=ytdlp_core
```

### Desktop

```bash
cd desktop-multiplatform
pytest -v
```

### Android

```bash
cd mobile-android
./gradlew test
./gradlew connectedAndroidTest  # requiere emulador/dispositivo
```

## Release

Automatizado via GitHub Actions al crear tag:

```bash
git tag v2.1.0
git push origin v2.1.0
```

Genera:
- Linux: `YourFreeDownloader-v2.1.0-Linux.tar.gz`
- Android Debug: `YourFreeDownloader-v2.1.0-Android-Debug.apk`
- Android Release: `YourFreeDownloader-v2.1.0-Android-Release.aab`

## Reportar issues

Usa las plantillas de GitHub Issues:

- **Bug**: Pasos para reproducir, esperado vs actual, logs
- **Feature**: Caso de uso, solución propuesta, alternativas
- **Pregunta**: Buscar issues existentes primero

## Código de conducta

- Respeto e inclusión
- Feedback constructivo
- Sin acoso ni discriminación
- Reportar violaciones a los maintainers

## Licencia

Al contribuir, aceptas que tus aportes se licencian bajo MIT.