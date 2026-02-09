# YouTube Downloader - Aplicación de Escritorio Multiplataforma

![Version](https://img.shields.io/badge/version-2.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![Python](https://img.shields.io/badge/python-3.8%2B-green)

## 📖 Descripción

Aplicación de escritorio multiplataforma para descargar videos y audio de YouTube con una interfaz gráfica moderna y amigable.

## ✨ Características

- 🎨 **Interfaz moderna** con CustomTkinter
- 🌓 **Tema oscuro/claro** intercambiable
- 📥 **Descarga de videos** en diferentes calidades (MP4)
- 🎵 **Extracción de audio** en formato MP3
- 📊 **Barra de progreso** en tiempo real
- 📁 **Selección de carpeta** de destino personalizada
- 📝 **Log de descarga** detallado
- 🔍 **Detección automática** de ffmpeg
- ✅ **Validación** de URLs de YouTube
- 💾 **Configuración persistente**
- 🚀 **Descargas simultáneas** (hasta 3)

## 🖥️ Plataformas Soportadas

- ✅ Windows 7/8/10/11
- ✅ Linux (Ubuntu, Debian, Fedora, Arch, etc.)

## 🔧 Requisitos

### Obligatorios del Sistema
- Python 3.8 o superior
- **Tk/Tcinter** (para interfaz gráfica)
  - Arch: `sudo pacman -S tk`
  - Ubuntu/Debian: `sudo apt install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
- Conexión a Internet

### Dependencias Python (se instalan automáticamente)
- `customtkinter` - Interfaz gráfica moderna
- `yt-dlp` - Motor de descarga de YouTube
- `pyinstaller` - Para compilar ejecutables (opcional)

### Opcional
- **FFmpeg** - Para conversión a MP3 y merge de video+audio
  - Windows: Se incluye en el ejecutable compilado
  - Linux: `sudo apt install ffmpeg` (Ubuntu/Debian), `sudo pacman -S ffmpeg` (Arch), etc.

## 📦 Instalación

### ⭐ Opción Recomendada: Usar Scripts Automáticos

Los scripts manejan automáticamente los entornos virtuales y las dependencias.

#### En Linux:
```bash
# Desde la raíz del proyecto
./start.sh

# O desde desktop-multiplatform
cd desktop-multiplatform
./scripts/run-linux.sh
```

#### En Windows:
```batch
cd desktop-multiplatform
scripts\run-windows.bat
```

> **💡 Nota para Linux:** En distribuciones modernas (Arch, Ubuntu 23.04+, Debian 12+), NO uses `pip install` directamente sin entorno virtual. Los scripts ya manejan esto correctamente.

### Opción 2: Instalación Manual (Avanzado)

```bash
# 1. Ir al directorio
cd desktop-multiplatform

# 2. Crear entorno virtual (OBLIGATORIO en Linux moderno)
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate  # Linux
# o
venv\Scripts\activate     # Windows

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar la aplicación
python src/yt-downlader.py
```

### Opción 3: Compilar ejecutable

#### En Linux:
```bash
cd desktop-multiplatform/scripts
./build-linux.sh
```

#### En Windows:
```batch
cd desktop-multiplatform\scripts
build-windows.bat
```

El ejecutable compilado estará en `build/dist/YouTubeDownloader/`

## 📖 Modo de Uso

1. **Ejecuta la aplicación** usando cualquiera de los métodos anteriores
2. **Pega una URL** de YouTube en el campo de entrada
3. **Selecciona el formato**:
   - Video: Elige la calidad deseada (360p, 720p, 1080p, etc.)
   - Audio: Solo MP3
4. **Elige la carpeta** de destino (opcional)
5. **Haz clic en Descargar** y espera a que termine

## 📂 Estructura del Proyecto

```
desktop-multiplatform/
├── src/
│   └── yt-downlader.py          # Código fuente principal
├── config/
│   ├── config.json              # Configuración de la app
│   └── YouTubeDownloader.spec   # Configuración PyInstaller
├── scripts/
│   ├── build-linux.sh           # Script de compilación Linux
│   ├── build-windows.bat        # Script de compilación Windows
│   ├── run-linux.sh             # Script de ejecución Linux
│   └── run-windows.bat          # Script de ejecución Windows
├── docs/
│   ├── LEEME.txt                # Documentación en español
│   ├── INSTRUCCIONES_*.md       # Instrucciones detalladas
│   └── README_COMPILACION.md    # Guía de compilación
├── resources/                   # Recursos (iconos, imágenes)
├── build/                       # Archivos de compilación
└── requirements.txt             # Dependencias Python
```

## 🔍 Solución de Problemas

### ❌ Error: "ModuleNotFoundError: No module named 'customtkinter'"

**Causa:** Intentaste ejecutar la app directamente con Python del sistema.

**✅ Solución:**
```bash
# Usa los scripts proporcionados que manejan entornos virtuales:
./scripts/run-linux.sh    # Linux
# o
scripts\run-windows.bat   # Windows
```

### ❌ Error: "externally-managed-environment" (Linux)

**Causa:** Python 3.11+ en sistemas modernos previene instalación global de paquetes.

**✅ Solución:** NO uses `pip install --break-system-packages`

En su lugar, usa los scripts que automáticamente crean entornos virtuales:
```bash
./scripts/run-linux.sh
```

**📚 Para más detalles:** Ver [TROUBLESHOOTING_LINUX.md](TROUBLESHOOTING_LINUX.md)

### Error: "FFmpeg not found"

**Linux:** Instala ffmpeg con tu gestor de paquetes
```bash
sudo apt install ffmpeg         # Ubuntu/Debian
sudo dnf install ffmpeg         # Fedora
sudo pacman -S ffmpeg          # Arch
```

**Windows:** FFmpeg está incluido en el ejecutable compilado

### Error: "No module named 'venv'"

**Ubuntu/Debian:**
```bash
sudo apt install python3-venv
```

**Fedora:**
```bash
sudo dnf install python3-virtualenv
```

### La descarga falla constantemente

- Verifica tu conexión a Internet
- Asegúrate de que la URL de YouTube sea válida
- Actualiza yt-dlp dentro del entorno virtual:
  ```bash
  source venv/bin/activate
  pip install --upgrade yt-dlp
  ```

### 📚 Guía Completa de Problemas

Para una guía detallada de solución de problemas en Linux, consulta:
**[TROUBLESHOOTING_LINUX.md](TROUBLESHOOTING_LINUX.md)**

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.

## 👤 Autor

**HanserlodXP**

## 🙏 Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Motor de descarga
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Framework de UI
- [FFmpeg](https://ffmpeg.org/) - Procesamiento de multimedia

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!
