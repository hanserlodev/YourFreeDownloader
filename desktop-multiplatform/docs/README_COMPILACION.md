# 🎯 GUÍA RÁPIDA DE COMPILACIÓN

## ⚡ Compilar en 4 pasos:

### 0️⃣ Integrar FFmpeg (IMPORTANTE):
```powershell
# Descargar ffmpeg desde: https://www.gyan.dev/ffmpeg/builds/
# Extraer y copiar ffmpeg.exe a: ffmpeg/bin/ffmpeg.exe
```
📖 **Ver guía detallada**: `INSTRUCCIONES_FFMPEG.md`

### 1️⃣ Instalar PyInstaller (si no lo tienes):
```powershell
pip install pyinstaller
```

### 2️⃣ Ejecutar compilación:
```powershell
.\compilar.bat
```
**O compilación rápida:**
```powershell
.\compilar-rapido.bat
```

### 3️⃣ ¡Listo!
Tu ejecutable estará en: `dist\YouTubeDownloader.exe`

---

## 📁 Estructura del proyecto recomendada:

```
YourFreeDownloader-Windows/
├── yt-downlader.py
├── compilar.bat
├── yt-downlader.spec
├── ffmpeg/                      ← ¡Agregar esto!
│   └── bin/
│       ├── ffmpeg.exe           ← Archivo necesario
│       └── ffprobe.exe          ← (Opcional)
└── YouTubeDownloader_Data/      ← Se crea automáticamente
    ├── config.json
    └── descargador.log
```

---

## ✅ ¿Qué archivos son importantes?

### ❌ NO NECESITAS distribuir:
- `yt-downlader.py` (código fuente)
- `compilar.bat` / `compilar-rapido.bat`
- `yt-downlader.spec`
- Carpetas `build/` y `__pycache__/`

### ✅ SOLO DISTRIBUYE:
- `YouTubeDownloader.exe` ← **¡SOLO ESTE ARCHIVO!**
- `LEEME.txt` (opcional, instrucciones para el usuario)

---

## 🔒 ¿Se perderán los archivos config.json y descargador.log?

### ¡NO! Están protegidos porque:

1. **El código detecta automáticamente** si está corriendo como .exe
2. **Crea la carpeta** `YouTubeDownloader_Data` donde sea que esté el .exe
3. **Guarda ahí** tanto `config.json` como `descargador.log`
4. **Persiste** entre ejecuciones

### Código implementado:
```python
def obtener_directorio_datos() -> Path:
    if getattr(sys, 'frozen', False):
        # Ejecutándose como EXE compilado
        app_dir = Path(sys.executable).parent / "YouTubeDownloader_Data"
    else:
        # Ejecutándose como script Python
        app_dir = Path(__file__).parent / "YouTubeDownloader_Data"
    
    app_dir.mkdir(exist_ok=True)  # Crea si no existe
    return app_dir
```

---

## 📊 Comparación de métodos:

| Método | Velocidad | Instalaciones |
|--------|-----------|---------------|
| `compilar.bat` | ⭐⭐⭐ | Instala dependencias automáticamente |
| `compilar-rapido.bat` | ⭐⭐⭐⭐⭐ | Requiere pyinstaller instalado |
| `pyinstaller yt-downlader.spec` | ⭐⭐⭐⭐⭐ | Requiere pyinstaller instalado |

---

## 🎉 ¡Todo está listo!

Tu aplicación ya está completamente preparada para ser compilada y distribuida. Los archivos importantes (`config.json` y `descargador.log`) funcionarán perfectamente y NO se perderán.

**Ejecuta `.\compilar.bat` y en unos minutos tendrás tu ejecutable listo!** 🚀
