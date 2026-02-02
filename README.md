# YourFreeDownloader - Proyecto Multiplataforma

![Version](https://img.shields.io/badge/version-2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 Descripción

**YourFreeDownloader** es un proyecto multiplataforma para descargar videos y audio de YouTube, disponible tanto para dispositivos móviles Android como para sistemas de escritorio Windows y Linux.

## 🎯 Plataformas Soportadas

- 📱 **Android** (API 24+) - Aplicación móvil nativa
- 🖥️ **Windows** (7/8/10/11) - Aplicación de escritorio
- 🐧 **Linux** (Todas las distros) - Aplicación de escritorio

## 📂 Estructura del Proyecto

```
YourFreeDownloader/
│
├── 📱 mobile-android/              # Aplicación Android
│   ├── src/                        # Código fuente Android
│   ├── build.gradle.kts            # Configuración Gradle
│   └── README.md                   # Documentación Android
│
├── 🖥️ desktop-multiplatform/       # Aplicación de Escritorio (Win/Linux)
│   ├── src/                        # Código fuente Python
│   │   └── yt-downlader.py         # Aplicación principal
│   ├── scripts/                    # Scripts de compilación y ejecución
│   │   ├── build-linux.sh          # Compilar para Linux
│   │   ├── build-windows.bat       # Compilar para Windows
│   │   ├── run-linux.sh            # Ejecutar en Linux
│   │   └── run-windows.bat         # Ejecutar en Windows
│   ├── config/                     # Archivos de configuración
│   ├── docs/                       # Documentación
│   ├── resources/                  # Recursos (iconos, etc.)
│   ├── requirements.txt            # Dependencias Python
│   └── README.md                   # Documentación Desktop
│
├── 📦 shared/                      # Código compartido (futuro)
│   └── (código común entre plataformas)
│
├── build.gradle.kts                # Configuración Gradle raíz (Android)
├── settings.gradle.kts             # Configuración del proyecto Android
├── gradle.properties               # Propiedades Gradle
└── README.md                       # Este archivo
```

## 🚀 Inicio Rápido

### Para la Aplicación de Escritorio (Windows/Linux)

#### Ejecutar desde código fuente:
```bash
cd desktop-multiplatform
pip install -r requirements.txt
python src/yt-downlader.py
```

#### O usar los scripts:
- **Linux**: `./desktop-multiplatform/scripts/run-linux.sh`
- **Windows**: `desktop-multiplatform\scripts\run-windows.bat`

#### Compilar ejecutable:
- **Linux**: `./desktop-multiplatform/scripts/build-linux.sh`
- **Windows**: `desktop-multiplatform\scripts\build-windows.bat`

### Para la Aplicación Móvil Android

```bash
cd mobile-android
./gradlew assembleDebug
```

O abre el proyecto `mobile-android` en Android Studio.

## ✨ Características

### Aplicación de Escritorio
- 🎨 Interfaz gráfica moderna con CustomTkinter
- 🌓 Tema oscuro/claro
- 📥 Descarga de videos en múltiples calidades
- 🎵 Extracción de audio MP3
- 📊 Progreso en tiempo real
- 💾 Configuración persistente

### Aplicación Móvil
- 📱 Interfaz nativa Android
- 📥 Descarga directa en dispositivo
- 🎵 Extracción de audio
- 💾 Gestión de descargas

## 🔧 Requisitos

### Aplicación de Escritorio
- Python 3.8+
- FFmpeg (opcional, para conversión de audio)
- Conexión a Internet

### Aplicación Móvil
- Android Studio
- JDK 11
- Android SDK API 36
- Dispositivo/Emulador con Android 7.0+

## 📚 Documentación Detallada

- [Documentación Aplicación de Escritorio](desktop-multiplatform/README.md)
- [Documentación Aplicación Android](mobile-android/README.md)

## 🛠️ Desarrollo

### Compilar para todas las plataformas:

#### Desktop - Linux:
```bash
cd desktop-multiplatform/scripts
./build-linux.sh
```

#### Desktop - Windows:
```batch
cd desktop-multiplatform\scripts
build-windows.bat
```

#### Móvil - Android:
```bash
cd mobile-android
./gradlew assembleRelease
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**HanserlodXP**

## 🙏 Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Motor de descarga de YouTube
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Framework de UI para Desktop
- [FFmpeg](https://ffmpeg.org/) - Procesamiento multimedia
- [Chaquopy](https://chaquo.com/chaquopy/) - Python en Android

## 🗺️ Roadmap

- [ ] Mejoras en la UI de Android
- [ ] Sincronización de descargas entre dispositivos
- [ ] Soporte para más plataformas de video
- [ ] Sistema de colas de descarga mejorado
- [ ] Versión para macOS
- [ ] Integración con servicios en la nube

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un [issue](https://github.com/hanserlodev/YourFreeDownloader/issues) en GitHub.

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!

🔄 Última actualización: Febrero 2026
