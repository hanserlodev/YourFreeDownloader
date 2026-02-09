# 🔧 Solución de Problemas Comunes - Linux

## ❌ Error: "ImportError: libtk8.6.so: cannot open shared object file"

### Causa
Este error significa que **Tk/Tcinter** no está instalado en tu sistema. Es un requisito del sistema operativo (no de Python) necesario para las interfaces gráficas con Tkinter/CustomTkinter.

El error completo se ve así:
```
ImportError: libtk8.6.so: cannot open shared object file: No such file or directory
```

### ✅ Solución: Instalar Tk en tu Sistema

**Arch Linux (tu sistema):**
```bash
sudo pacman -S tk
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**openSUSE:**
```bash
sudo zypper install python3-tk
```

**Después de instalar**, ejecuta nuevamente:
```bash
./start.sh
```

### 🔍 Verificar si Tk está Instalado

```bash
python3 -c "import tkinter; print('✅ Tk instalado correctamente')"
```

Si ves el mensaje "✅ Tk instalado correctamente", entonces está bien instalado.

---

## ❌ Error: "ModuleNotFoundError: No module named 'customtkinter'"

### Causa
Este error ocurre cuando intentas ejecutar la aplicación directamente con Python del sistema sin usar un entorno virtual.

### ✅ Solución Recomendada: Usar el Script de Inicio

**La forma más fácil:**
```bash
./start.sh
```

Este script automáticamente:
- Crea un entorno virtual si no existe
- Instala todas las dependencias necesarias
- Ejecuta la aplicación

### ✅ Solución Manual: Crear Entorno Virtual

Si prefieres hacerlo manualmente:

```bash
# 1. Ir al directorio de desktop
cd desktop-multiplatform

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python src/yt-downlader.py
```

## ❌ Error: "externally-managed-environment"

### Causa
Python 3.11+ en distribuciones modernas (como Arch, Ubuntu 23.04+, Debian 12+) implementa PEP 668, que previene instalar paquetes globalmente con pip para proteger el sistema.

### ❌ NO Hagas Esto:
```bash
pip install customtkinter --break-system-packages  # ¡No recomendado!
```

### ✅ Haz Esto en Su Lugar:

**Opción 1: Usa el script de inicio (recomendado)**
```bash
./start.sh
```

**Opción 2: Crea un entorno virtual manualmente**
```bash
cd desktop-multiplatform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/yt-downlader.py
```

**Opción 3: Usa pipx (solo para instalar la app permanentemente)**
```bash
# Instalar pipx
sudo pacman -S python-pipx  # Arch
# o
sudo apt install pipx       # Ubuntu/Debian

# Instalar la aplicación
pipx install customtkinter
pipx install yt-dlp
```

## ❌ Error: "No module named 'venv'"

### Causa
El módulo venv no está instalado (común en algunos sistemas).

### ✅ Solución por Distribución:

**Arch Linux:**
```bash
# venv viene incluido con python, no necesitas hacer nada
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-venv
```

**Fedora:**
```bash
sudo dnf install python3-virtualenv
```

**openSUSE:**
```bash
sudo zypper install python3-virtualenv
```

## ❌ Error al crear entorno virtual

### Si ves errores sobre pip o setuptools:

```bash
# Arch
sudo pacman -S python-pip

# Ubuntu/Debian
sudo apt install python3-pip python3-venv

# Fedora
sudo dnf install python3-pip python3-virtualenv
```

## 🔍 Verificar que Todo Está Correcto

```bash
# Verificar Python
python3 --version  # Debe ser 3.8 o superior

# Verificar que venv está disponible
python3 -m venv --help

# Verificar FFmpeg (opcional)
ffmpeg -version
```

## 📦 Instalar FFmpeg (Para conversión MP3)

**Arch:**
```bash
sudo pacman -S ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Fedora:**
```bash
sudo dnf install ffmpeg
```

## 🚀 Resumen de Comandos Rápidos

### Inicio Simple (Recomendado):
```bash
./start.sh
```

### O ir paso a paso:
```bash
cd desktop-multiplatform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/yt-downlader.py
```

### Compilar ejecutable:
```bash
cd desktop-multiplatform
./scripts/build-linux.sh
```

### Limpiar y empezar de nuevo:
```bash
cd desktop-multiplatform
rm -rf venv
./scripts/run-linux.sh  # Recreará todo automáticamente
```

## 🆘 Aún Tienes Problemas?

1. **Asegúrate de estar usando Python 3.8 o superior:**
   ```bash
   python3 --version
   ```

2. **Verifica los permisos de los scripts:**
   ```bash
   chmod +x start.sh
   chmod +x desktop-multiplatform/scripts/*.sh
   ```

3. **Revisa los logs de error completos** y busca la línea específica del error.

4. **Prueba actualizar pip en tu entorno virtual:**
   ```bash
   source desktop-multiplatform/venv/bin/activate
   pip install --upgrade pip setuptools wheel
   pip install -r desktop-multiplatform/requirements.txt
   ```

## 💡 Buenas Prácticas

1. **Siempre usa entornos virtuales** para proyectos Python
2. **Nunca uses `--break-system-packages`** a menos que sepas exactamente lo que haces
3. **Usa los scripts proporcionados** (`start.sh`, `run-linux.sh`) en lugar de ejecutar Python directamente
4. **Mantén tu entorno virtual actualizado:**
   ```bash
   source venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

---

📝 **Nota sobre Arch Linux**: Arch Linux usa Python 3.14 que implementa estrictamente PEP 668. Los entornos virtuales son la forma correcta y recomendada de manejar dependencias de proyectos Python.
