# ⚡ Solución Rápida: Error de Tk/Tcinter

## 🔴 El Error que Viste:

```
ImportError: libtk8.6.so: cannot open shared object file: No such file or directory
```

## ✅ Solución en 1 Comando:

### Arch Linux:
```bash
sudo pacman -S tk
```

### Ubuntu/Debian:
```bash
sudo apt install python3-tk
```

### Fedora:
```bash
sudo dnf install python3-tkinter
```

## 🚀 Después de Instalar:

```bash
./start.sh
```

Y listo! La aplicación debería funcionar correctamente.

---

## 🤔 ¿Por qué pasó esto?

CustomTkinter (la biblioteca de interfaz gráfica) depende de **Tkinter**, que a su vez necesita las bibliotecas **Tk/Tcl** instaladas en tu sistema operativo.

Estas bibliotecas NO se pueden instalar con `pip` porque son dependencias del sistema, no de Python.

## 📋 Lista de Verificación Completa:

- [ ] Python 3.8+ instalado
- [ ] Tk/Tcinter instalado (este paso)
- [ ] FFmpeg instalado (opcional, para MP3)
- [ ] Ejecutar `./start.sh`

---

**Documentación Completa:** [TROUBLESHOOTING_LINUX.md](desktop-multiplatform/TROUBLESHOOTING_LINUX.md)
