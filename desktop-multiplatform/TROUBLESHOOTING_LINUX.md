# Troubleshooting Linux

## Error: "ImportError: libtk8.6.so: cannot open shared object file"

**Causa**: Tk/Tkinter no está instalado. Es requisito del sistema (no de Python) para interfaces gráficas con Tkinter/CustomTkinter.

**Solución**: Instala Tk según tu distribución:

```bash
# Arch Linux
sudo pacman -S tk

# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# openSUSE
sudo zypper install python3-tk
```

Luego vuelve a ejecutar:
```bash
./start.sh
```

**Verificar**:
```bash
python3 -c "import tkinter; print('Tk instalado correctamente')"
```

---

## Error: "ModuleNotFoundError: No module named 'customtkinter'"

**Causa**: Intentaste ejecutar la app con Python del sistema sin entorno virtual.

**Solución recomendada**: Usa el script de inicio
```bash
./start.sh
```
El script crea el venv, instala dependencias y ejecuta la app.

**Solución manual**:
```bash
cd desktop-multiplatform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/yt-downlader.py
```

---

## Error: "externally-managed-environment"

**Causa**: Python 3.11+ en distros modernas (Arch, Ubuntu 23.04+, Debian 12+) implementa PEP 668, que bloquea `pip install` global.

**NO hagas esto**:
```bash
pip install customtkinter --break-system-packages  # No recomendado
```

**Haz esto en su lugar**:

Opción 1 - Script de inicio (recomendado):
```bash
./start.sh
```

Opción 2 - Entorno virtual manual:
```bash
cd desktop-multiplatform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/yt-downlader.py
```

Opción 3 - pipx (solo para instalar app permanentemente):
```bash
# Arch
sudo pacman -S python-pipx
# Ubuntu/Debian
sudo apt install pipx

pipx install customtkinter
pipx install yt-dlp
```

---

## Error: "No module named 'venv'"

**Solución por distribución**:

```bash
# Ubuntu/Debian
sudo apt install python3-venv

# Fedora
sudo dnf install python3-virtualenv

# openSUSE
sudo zypper install python3-virtualenv

# Arch: venv viene incluido con python
```

---

## Error al crear entorno virtual (pip/setuptools)

```bash
# Arch
sudo pacman -S python-pip

# Ubuntu/Debian
sudo apt install python3-pip python3-venv

# Fedora
sudo dnf install python3-pip python3-virtualenv
```

---

## Verificación rápida

```bash
# Python >= 3.8
python3 --version

# venv disponible
python3 -m venv --help

# FFmpeg (opcional, para MP3)
ffmpeg -version
```

---

## Instalar FFmpeg (conversión MP3)

```bash
# Arch
sudo pacman -S ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

---

## Comandos de referencia

**Inicio simple (recomendado)**:
```bash
./start.sh
```

**Paso a paso**:
```bash
cd desktop-multiplatform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/yt-downlader.py
```

**Compilar ejecutable**:
```bash
cd desktop-multiplatform
./scripts/build-linux.sh
```

**Limpiar y reiniciar**:
```bash
cd desktop-multiplatform
rm -rf venv
./scripts/run-linux.sh  # Recrea todo automáticamente
```

---

## Si sigues teniendo problemas

1. **Python 3.8+**:
   ```bash
   python3 --version
   ```

2. **Permisos de scripts**:
   ```bash
   chmod +x start.sh
   chmod +x desktop-multiplatform/scripts/*.sh
   ```

3. **Revisa logs completos** y busca la línea exacta del error.

4. **Actualiza pip en el venv**:
   ```bash
   source desktop-multiplatform/venv/bin/activate
   pip install --upgrade pip setuptools wheel
   pip install -r desktop-multiplatform/requirements.txt
   ```

---

## Buenas prácticas

1. **Siempre usa entornos virtuales** para proyectos Python
2. **Nunca uses `--break-system-packages`** salvo que sepas exactamente qué haces
3. **Usa los scripts proporcionados** (`start.sh`, `run-linux.sh`) en lugar de ejecutar Python directamente
4. **Mantén tu venv actualizado**:
   ```bash
   source venv/bin/activate
   pip install --upgrade -r requirements.txt
   ```

---

**Nota sobre Arch Linux**: Arch usa Python 3.14 que implementa estrictamente PEP 668. Los entornos virtuales son la forma correcta y recomendada de manejar dependencias de proyectos Python.