# 🚀 Inicio Rápido - YourFreeDownloader

## ✅ ¡Configuración Mejorada!

He actualizado el proyecto para evitar problemas con entornos Python modernos (PEP 668).

## 🎯 Formas de Ejecutar la Aplicación de Escritorio

### 1️⃣ **Forma Más Simple (Recomendada para Linux):**

Desde la raíz del proyecto:
```bash
./start.sh
```

Este script:
- ✅ Verifica Python
- ✅ Crea automáticamente un entorno virtual
- ✅ Instala todas las dependencias
- ✅ Ejecuta la aplicación
- ✅ No requiere permisos sudo
- ✅ No afecta tu sistema

### 2️⃣ **Desde el directorio desktop-multiplatform:**

```bash
cd desktop-multiplatform
./scripts/run-linux.sh
```

### 3️⃣ **Compilar un ejecutable:**

```bash
cd desktop-multiplatform
./scripts/build-linux.sh
```

El ejecutable estará en `build/dist/YouTubeDownloader/`

## 📝 Lo Que Se Solucionó

### ❌ Antes (Problemas):
```bash
python yt-downlader.py
# ❌ ModuleNotFoundError: No module named 'customtkinter'

pip install customtkinter
# ❌ error: externally-managed-environment
```

### ✅ Ahora (Funciona):
```bash
./start.sh
# ✅ Todo funciona automáticamente
```

## 🔧 ¿Qué Cambió?

1. **Script de inicio rápido** (`start.sh`)
   - Crea y maneja entornos virtuales automáticamente
   - Instala dependencias si es necesario
   - Verifica FFmpeg (opcional)

2. **Scripts mejorados de ejecución**
   - `desktop-multiplatform/scripts/run-linux.sh` - Ahora crea venv automáticamente
   - `desktop-multiplatform/scripts/build-linux.sh` - Mejorado con mejor manejo de errores

3. **Documentación actualizada**
   - [TROUBLESHOOTING_LINUX.md](desktop-multiplatform/TROUBLESHOOTING_LINUX.md) - Guía completa de problemas comunes
   - READMEs actualizados con mejores instrucciones

## 🐧 Instalación de Requisitos del Sistema

### 1. Instalar Tk/Tcinter (Obligatorio para GUI)

Este es un requisito del sistema para la interfaz gráfica:

```bash
# Arch Linux (tu sistema)
sudo pacman -S tk

# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

### 2. Instalar FFmpeg (Opcional para conversión a MP3)

Para conversión a MP3, instala FFmpeg:

```bash
# Arch Linux (tu sistema)
sudo pacman -S ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

## 📚 Más Información

- **README principal:** [README.md](README.md)
- **README Desktop:** [desktop-multiplatform/README.md](desktop-multiplatform/README.md)
- **Problemas en Linux:** [desktop-multiplatform/TROUBLESHOOTING_LINUX.md](desktop-multiplatform/TROUBLESHOOTING_LINUX.md)

## 🎉 ¡A Probar!

```bash
# Simplemente ejecuta:
./start.sh

# La primera vez tomará un momento instalando dependencias
# Las siguientes veces será instantáneo
```

---

💡 **Tip:** Si algo falla, consulta [TROUBLESHOOTING_LINUX.md](desktop-multiplatform/TROUBLESHOOTING_LINUX.md)
