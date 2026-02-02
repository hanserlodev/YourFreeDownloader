# 🚀 Instrucciones para Compilar con PyInstaller

## 📋 Requisitos Previos

1. **Python 3.8+** instalado
2. **Dependencias** instaladas:
   ```powershell
   pip install customtkinter yt-dlp pyinstaller
   ```
3. **ffmpeg** (opcional pero recomendado para conversión de audio)

---

## 🔨 Método 1: Compilación Automática (RECOMENDADO)

### Ejecuta el script de compilación:
```powershell
.\compilar.bat
```

Este script hará:
- ✅ Verificar Python
- ✅ Instalar dependencias
- ✅ Limpiar compilaciones anteriores
- ✅ Compilar con PyInstaller
- ✅ Verificar el ejecutable generado

### Resultado:
El ejecutable estará en: `dist\YouTubeDownloader.exe`

---

## 🔧 Método 2: Compilación Manual

### Usando el archivo .spec:
```powershell
pyinstaller yt-downlader.spec
```

### O compilación directa:
```powershell
pyinstaller --onefile --windowed --name "YouTubeDownloader" `
  --hidden-import customtkinter `
  --hidden-import yt_dlp `
  --hidden-import PIL._tkinter_finder `
  --exclude-module matplotlib `
  --exclude-module pandas `
  --exclude-module numpy `
  yt-downlader.py
```

---

## 📁 Archivos Importantes

### Archivos que se crean automáticamente:

El ejecutable creará una carpeta `YouTubeDownloader_Data` junto al .exe con:

- **`config.json`**: Configuración de la aplicación
  - Última carpeta de descarga
  - Calidad preferida
  - Preferencia de solo audio
  - Tamaño de ventana

- **`descargador.log`**: Registro de actividad
  - Historial de descargas
  - Errores y advertencias
  - Información de debug

### 🔍 Ubicación de los archivos:

```
📦 YouTubeDownloader.exe          ← Ejecutable principal
└── 📂 YouTubeDownloader_Data/    ← Se crea automáticamente
    ├── 📄 config.json             ← Configuración persistente
    └── 📄 descargador.log         ← Registro de actividad
```

---

## ⚙️ Funcionamiento con PyInstaller

### ✅ NO SE PERDERÁ NADA porque:

1. **Detección automática**: El código detecta si está corriendo como .exe o como script Python
2. **Carpeta de datos**: Crea `YouTubeDownloader_Data` automáticamente
3. **Persistencia**: `config.json` y `descargador.log` se guardan ahí
4. **Portabilidad**: Puedes mover el .exe con su carpeta _Data a cualquier lugar

### 📝 Código implementado:

```python
def obtener_directorio_datos() -> Path:
    if getattr(sys, 'frozen', False):
        # Ejecutándose como EXE
        app_dir = Path(sys.executable).parent / "YouTubeDownloader_Data"
    else:
        # Ejecutándose como script Python
        app_dir = Path(__file__).parent / "YouTubeDownloader_Data"
    
    app_dir.mkdir(exist_ok=True)
    return app_dir
```

---

## 🎯 Distribución del Ejecutable

### Para distribuir tu aplicación:

1. **Copia el archivo**: `YouTubeDownloader.exe`
2. **La carpeta de datos** se creará automáticamente al ejecutarlo
3. **ffmpeg** (opcional): El usuario debe tenerlo instalado para:
   - Conversión a MP3
   - Merge de video + audio de alta calidad

### 📦 Distribución completa (recomendado):

```
📦 YouTubeDownloader_v2.0/
├── 📄 YouTubeDownloader.exe     ← Ejecutable principal
├── 📄 README.txt                ← Instrucciones de uso
└── 📄 ffmpeg_info.txt           ← Link de descarga de ffmpeg
```

---

## ❓ Preguntas Frecuentes

### ¿Se perderán mis configuraciones?
**NO**. El archivo `config.json` se guarda en `YouTubeDownloader_Data` y persiste entre ejecuciones.

### ¿Necesito Python instalado para ejecutar el .exe?
**NO**. PyInstaller empaqueta todo lo necesario en el ejecutable.

### ¿Puedo mover el .exe a otra carpeta?
**SÍ**. Puedes moverlo libremente. La carpeta `YouTubeDownloader_Data` se creará automáticamente en la nueva ubicación.

### ¿Qué pasa con el log de descargas?
El archivo `descargador.log` se mantiene en `YouTubeDownloader_Data` y guarda todo el historial.

### ¿Necesito ffmpeg?
Es **opcional** pero **recomendado** para:
- Conversión a MP3
- Merge de video + audio de alta calidad
- Mejor compatibilidad de formatos

---

## 🐛 Solución de Problemas

### Error: "No module named 'customtkinter'"
```powershell
pip install customtkinter
```

### El .exe es muy grande
Es normal. PyInstaller empaqueta Python completo + dependencias.
Tamaño típico: 40-60 MB

### Error al ejecutar el .exe
1. Verifica que tienes permisos de escritura en la carpeta
2. Desactiva temporalmente el antivirus (puede bloquear el .exe)
3. Ejecuta como administrador si es necesario

### La carpeta _Data no se crea
Verifica que el .exe tiene permisos de escritura en su directorio.

---

## 📞 Soporte

**Autor**: HanserlodXP  
**Versión**: 2.0  
**Fecha**: 11/11/2025  

---

## 🎉 ¡Listo para Distribuir!

Tu aplicación está completamente preparada para ser distribuida como un ejecutable standalone. Los archivos `config.json` y `descargador.log` funcionarán perfectamente y persistirán entre ejecuciones.
