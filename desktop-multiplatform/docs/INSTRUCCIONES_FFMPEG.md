# 🎬 Cómo Integrar FFmpeg en el Proyecto

## 📥 Paso 1: Descargar FFmpeg

### Opción A: Descarga desde el sitio oficial (Recomendado)

1. Ve a: https://www.gyan.dev/ffmpeg/builds/
2. Descarga: **ffmpeg-release-essentials.zip** (versión más ligera)
3. O descarga desde: https://github.com/BtbN/FFmpeg-Builds/releases
   - Busca: `ffmpeg-master-latest-win64-gpl.zip`

### Opción B: Descarga rápida

Link directo (Gyan.dev):
```
https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
```

---

## 📂 Paso 2: Extraer FFmpeg en el Proyecto

### Estructura recomendada:

Extrae el archivo ZIP y copia la carpeta `bin` con `ffmpeg.exe` dentro:

```
YourFreeDownloader-Windows/
├── yt-downlader.py
├── compilar.bat
├── yt-downlader.spec
└── ffmpeg/                    ← Crear esta carpeta
    └── bin/                   ← Copiar carpeta bin aquí
        ├── ffmpeg.exe         ← Archivo principal
        └── ffprobe.exe        ← (Opcional pero recomendado)
```

### Alternativas aceptadas:

El código busca ffmpeg en estas ubicaciones (en orden de prioridad):

1. `ffmpeg/bin/ffmpeg.exe` ← **RECOMENDADO**
2. `ffmpeg/ffmpeg.exe`
3. `bin/ffmpeg.exe`
4. `ffmpeg.exe` (raíz del proyecto)

---

## ✅ Paso 3: Verificar la Integración

### Método 1: Ejecutar el script Python

```powershell
python yt-downlader.py
```

Deberías ver en el log:
```
✅ FFmpeg encontrado en: C:\...\ffmpeg\bin\ffmpeg.exe
```

### Método 2: Verificar manualmente

Asegúrate de que el archivo existe:
```powershell
dir ffmpeg\bin\ffmpeg.exe
```

Debería mostrar:
```
ffmpeg.exe
```

---

## 🔨 Paso 4: Compilar con FFmpeg Incluido

Cuando compiles con PyInstaller, ffmpeg se incluirá automáticamente:

```powershell
.\compilar.bat
```

O:

```powershell
pyinstaller yt-downlader.spec
```

Durante la compilación verás:
```
✅ ffmpeg encontrado: ffmpeg\bin\ffmpeg.exe
✅ ffprobe encontrado: ffmpeg\bin\ffprobe.exe
```

---

## 📦 Resultado Final

Después de compilar, tu ejecutable:

1. **Incluye ffmpeg empaquetado** dentro del .exe
2. **No necesita instalación** de ffmpeg en el sistema del usuario
3. **Funciona de inmediato** en cualquier Windows

### Tamaño aproximado:

- Sin ffmpeg: ~40-50 MB
- Con ffmpeg: **~60-80 MB** (totalmente standalone)

---

## 🎯 Ventajas de Incluir FFmpeg

✅ **Todo en uno**: Usuario no necesita instalar nada
✅ **Portabilidad**: Funciona en cualquier Windows sin configuración
✅ **Simplicidad**: Copia y ejecuta, ¡listo!
✅ **Profesional**: Aplicación completa y autosuficiente

---

## 🔍 Solución de Problemas

### ❌ "ffmpeg no encontrado en el proyecto"

**Causa**: No copiaste ffmpeg.exe en la ubicación correcta

**Solución**:
1. Verifica que `ffmpeg\bin\ffmpeg.exe` existe
2. O usa una de las ubicaciones alternativas
3. Re-ejecuta la compilación

### ❌ "Error al compilar: No module named 'pathlib'"

**Causa**: Python muy antiguo

**Solución**:
```powershell
pip install pathlib
```

### ❌ El .exe es muy grande (>100 MB)

**Causa**: ffmpeg completo es pesado

**Solución**: Es normal. Opciones:
- Usar la versión "essentials" de ffmpeg (más liviana)
- Aceptar el tamaño (60-80 MB es razonable para una app standalone)
- Usar UPX compression (ya incluido en .spec con `upx=True`)

---

## 📊 Comparación de Versiones de FFmpeg

| Versión | Tamaño | Recomendación |
|---------|--------|---------------|
| **essentials** | ~70 MB | ✅ **Recomendado** - Suficiente para el proyecto |
| **full** | ~120 MB | ⚠️ Innecesario - Incluye encoders extra |
| **shared** | ~50 MB | ❌ No funciona - Requiere DLLs adicionales |

---

## 🚀 Quick Start (Resumen)

```powershell
# 1. Descargar ffmpeg
# Ir a: https://www.gyan.dev/ffmpeg/builds/
# Descargar: ffmpeg-release-essentials.zip

# 2. Crear carpeta y copiar
mkdir ffmpeg\bin
# Copiar ffmpeg.exe y ffprobe.exe a ffmpeg\bin\

# 3. Verificar
python yt-downlader.py
# Ver log: "✅ FFmpeg encontrado..."

# 4. Compilar
.\compilar.bat
# ¡Listo! Tu .exe incluye ffmpeg
```

---

## 📝 Notas Importantes

- ✅ FFmpeg es **software libre** (GPL/LGPL)
- ✅ Puedes **distribuirlo** con tu aplicación
- ✅ **No requiere licencia comercial** para uso personal
- ⚠️ El .exe resultante será **solo para Windows**
- 💡 Para Linux/Mac necesitarías las versiones respectivas de ffmpeg

---

## 🎉 ¡Todo Listo!

Una vez completados estos pasos, tu aplicación:
- ✅ Incluye ffmpeg integrado
- ✅ Funciona sin instalación adicional
- ✅ Es totalmente portable
- ✅ Está lista para distribuir

**¡Disfruta de tu aplicación completamente autosuficiente!** 🚀
