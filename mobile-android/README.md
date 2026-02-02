# YourFreeDownloader - Aplicación Móvil Android

![Platform](https://img.shields.io/badge/platform-Android-green)
![MinSDK](https://img.shields.io/badge/minSdk-24-blue)
![TargetSDK](https://img.shields.io/badge/targetSdk-36-blue)

## 📖 Descripción

Aplicación móvil Android para descargar videos y audio de YouTube directamente en tu dispositivo.

## ✨ Características

- 📥 Descarga de videos de YouTube
- 🎵 Extracción de audio
- 📱 Interfaz nativa Android
- 🔄 Integración con Python backend
- 💾 Gestión de descargas

## 🔧 Requisitos de Desarrollo

- Android Studio Arctic Fox o superior
- JDK 11
- Gradle 7.0+
- Android SDK API 36
- Chaquopy Plugin (para integración con Python)

## 📦 Configuración del Proyecto

1. **Abrir el proyecto**:
   ```bash
   cd mobile-android
   ```

2. **Sincronizar Gradle**:
   - Abre Android Studio
   - File → Open → Selecciona la carpeta `mobile-android`
   - Espera a que Gradle sincronice

3. **Configurar SDK**:
   - Tools → SDK Manager
   - Asegúrate de tener Android SDK 36 instalado

## 🏗️ Compilar la Aplicación

### Desde Android Studio:
1. Build → Build Bundle(s) / APK(s) → Build APK(s)
2. El APK estará en `mobile-android/build/outputs/apk/`

### Desde línea de comandos:
```bash
cd mobile-android
./gradlew assembleDebug       # Para versión debug
./gradlew assembleRelease     # Para versión release
```

## 📂 Estructura del Proyecto

```
mobile-android/
├── build.gradle.kts           # Configuración Gradle del módulo
├── proguard-rules.pro         # Reglas ProGuard
└── src/
    ├── main/
    │   ├── AndroidManifest.xml
    │   ├── java/com/hanserlod/  # Código Java/Kotlin
    │   ├── python/              # Scripts Python (Chaquopy)
    │   │   └── hanserlod.py
    │   └── res/                 # Recursos Android
    │       ├── drawable/
    │       ├── layout/
    │       ├── mipmap-*/
    │       ├── values/
    │       └── xml/
    ├── androidTest/             # Tests instrumentados
    └── test/                    # Tests unitarios
```

## 🚀 Ejecutar en Dispositivo/Emulador

1. Conecta un dispositivo Android o inicia un emulador
2. En Android Studio: Run → Run 'app'
3. O desde terminal:
   ```bash
   ./gradlew installDebug
   ```

## 🔍 Características Técnicas

- **Lenguaje**: Kotlin + Java
- **Min SDK**: Android 7.0 (API 24)
- **Target SDK**: Android 15 (API 36)
- **Arquitectura**: ARM64-v8a, x86_64
- **Backend**: Python (vía Chaquopy)

## 📝 Notas de Desarrollo

- El proyecto utiliza **Chaquopy** para ejecutar código Python en Android
- Los scripts Python están en `src/main/python/`
- Se requiere configuración especial de ProGuard para el release

## 🐛 Solución de Problemas

### Error: "SDK not found"
- Configura `ANDROID_HOME` en tus variables de entorno
- O configura el SDK en Android Studio

### Error de compilación de Gradle
```bash
./gradlew clean
./gradlew build --refresh-dependencies
```

### Error con Chaquopy
- Verifica que el plugin esté correctamente configurado en `build.gradle.kts`
- Asegúrate de tener las dependencias de Python especificadas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

**HanserlodXP**

---

📱 Desarrollado con ❤️ para Android
