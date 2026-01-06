"""
Descargador de YouTube con interfaz gráfica moderna - Versión 2.0
=================================================================

Este módulo implementa una aplicación de escritorio para descargar videos y audio
de YouTube utilizando CustomTkinter para una interfaz gráfica moderna y yt-dlp 
para el procesamiento de descargas.

Características:
- 🎨 Interfaz moderna con CustomTkinter
- 🌓 Tema oscuro/claro intercambiable
- 📥 Descarga de videos en diferentes calidades
- 🎵 Extracción de solo audio en formato MP3
- 📊 Barra de progreso real durante la descarga
- 📁 Selección de carpeta de destino
- 📝 Log de descarga en tiempo real
- 🔍 Detección automática de ffmpeg
- ✅ Validación de URLs de YouTube
- 🛡️ Manejo mejorado de errores
- 💾 Guardar/cargar configuración

Dependencias:
- customtkinter: pip install customtkinter (para interfaz moderna)
- tkinter (incluido en Python estándar)
- yt-dlp: pip install yt-dlp
- ffmpeg: debe estar instalado en el sistema

Autor: HanserlodXP
Fecha: 11/11/2025
Versión: 2.0
"""

import os
import sys
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from concurrent.futures import ThreadPoolExecutor
import yt_dlp # type: ignore
from typing import Any, Optional, Dict
from pathlib import Path
import re
import json
import shutil
import logging
from datetime import datetime
import urllib.request
import socket

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# =============================================================================
# THREAD POOL Y CACHÉ
# =============================================================================

# Executor para manejar múltiples descargas simultáneas
executor = ThreadPoolExecutor(max_workers=3)

# Caché de información de videos consultados
cache_videos: Dict[str, Dict[str, Any]] = {}

# =============================================================================
# RUTAS DE ARCHIVOS (Compatibilidad con PyInstaller)
# =============================================================================

def obtener_directorio_datos() -> Path:
    """
    Obtiene el directorio donde se guardarán los archivos de configuración y logs.
    Compatible con PyInstaller y ejecución normal.
    
    Returns:
        Path: Ruta al directorio de datos de la aplicación
    """
    if getattr(sys, 'frozen', False):
        # Si está ejecutándose como EXE compilado con PyInstaller
        # Usar carpeta junto al ejecutable
        app_dir = Path(sys.executable).parent / "YouTubeDownloader_Data"
    else:
        # Si está ejecutándose como script Python normal
        # Usar carpeta del script
        app_dir = Path(__file__).parent / "YouTubeDownloader_Data"
    
    # Crear directorio si no existe
    app_dir.mkdir(exist_ok=True)
    return app_dir

# Directorio de datos de la aplicación
DIRECTORIO_DATOS = obtener_directorio_datos()

# Rutas de archivos
RUTA_CONFIG = DIRECTORIO_DATOS / "config.json"
RUTA_LOG = DIRECTORIO_DATOS / "descargador.log"

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================

def encontrar_ffmpeg() -> Optional[str]:
    """
    Busca automáticamente la ubicación de ffmpeg en el sistema.
    
    Returns:
        str | None: Ruta a ffmpeg si se encuentra, None en caso contrario
    
    Proceso:
    1. Busca ffmpeg en la carpeta del ejecutable/proyecto (PRIORIDAD)
    2. Busca ffmpeg empaquetado con PyInstaller (_MEIPASS)
    3. Busca ffmpeg en el PATH del sistema
    4. Verifica rutas comunes según el sistema operativo
    5. Retorna la primera ruta válida encontrada
    """
    # PRIORIDAD 1: Buscar en _MEIPASS (carpeta temporal de PyInstaller)
    if getattr(sys, 'frozen', False):
        # Ejecutándose como EXE compilado
        # PyInstaller crea una carpeta temporal _MEIPASS con los archivos empaquetados
        if hasattr(sys, '_MEIPASS'):
            meipass_path = Path(sys._MEIPASS) / "ffmpeg" / "ffmpeg.exe"  # type: ignore
            if meipass_path.exists():
                return str(meipass_path)
        
        # Buscar junto al ejecutable
        base_path = Path(sys.executable).parent
    else:
        # Ejecutándose como script Python
        base_path = Path(__file__).parent
    
    # PRIORIDAD 2: Buscar en la carpeta del proyecto/ejecutable
    rutas_proyecto = [
        base_path / "ffmpeg" / "bin" / "ffmpeg.exe",  # ffmpeg/bin/ffmpeg.exe
        base_path / "ffmpeg" / "ffmpeg.exe",          # ffmpeg/ffmpeg.exe
        base_path / "bin" / "ffmpeg.exe",             # bin/ffmpeg.exe
        base_path / "ffmpeg.exe",                     # ffmpeg.exe (raíz)
    ]
    
    for ruta in rutas_proyecto:
        if ruta.exists():
            return str(ruta)
    
    # PRIORIDAD 3: Buscar ffmpeg en el PATH del sistema
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # PRIORIDAD 4: Rutas comunes del sistema
    rutas_sistema = [
        r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        "/usr/bin/ffmpeg",
        "/usr/local/bin/ffmpeg",
    ]
    
    for ruta in rutas_sistema:
        if os.path.exists(ruta):
            return ruta
    
    return None

# Detectar ffmpeg automáticamente
FFMPEG_PATH = encontrar_ffmpeg()

def validar_url_youtube(url: str) -> bool:
    """
    Valida si una URL pertenece a YouTube con verificación mejorada.
    
    Args:
        url: URL a validar
    
    Returns:
        bool: True si es una URL válida de YouTube
    """
    # Patrones más estrictos para YouTube
    patrones = [
        r'^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/embed/[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/v/[\w-]+',
        r'^(https?://)?youtu\.be/[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/shorts/[\w-]+',
    ]
    
    return any(re.match(patron, url) for patron in patrones)

def verificar_conectividad(url: str, timeout: int = 3) -> bool:
    """
    Verifica si hay conectividad con YouTube.
    
    Args:
        url: URL a verificar
        timeout: Tiempo de espera en segundos
    
    Returns:
        bool: True si hay conectividad
    """
    try:
        socket.setdefaulttimeout(timeout)
        urllib.request.urlopen('https://www.youtube.com', timeout=timeout)
        return True
    except:
        return False

def cargar_configuracion() -> dict: # type: ignore
    """
    Carga la configuración desde archivo config.json.
    
    Returns:
        dict: Configuración cargada o configuración por defecto
    """
    try:
        with open(RUTA_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {  # type: ignore
            "ultima_carpeta": "",
            "calidad_preferida": "",
            "solo_audio_por_defecto": False,
            "ventana_ancho": 700,
            "ventana_alto": 600
        }

def guardar_configuracion(config: dict): # type: ignore
    """
    Guarda la configuración en archivo config.json.
    
    Args:
        config: Diccionario con la configuración a guardar
    """
    try:
        with open(RUTA_CONFIG, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar configuración: {e}")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(RUTA_LOG, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Cargar configuración inicial
config_app = cargar_configuracion() # type: ignore

# =============================================================================
# INICIALIZACIÓN DE LA INTERFAZ
# =============================================================================

# Crear ventana principal
ventana = ctk.CTk()
ventana.title("Descargador de YouTube v2.0  - by HanserlodXP")
ventana.geometry(f"{config_app.get('ventana_ancho', 700)}x{config_app.get('ventana_alto', 600)}") # type: ignore

# =============================================================================
# VARIABLES GLOBALES DE ESTADO
# =============================================================================

# Variable para almacenar la ruta de destino seleccionada
ruta_destino = ctk.StringVar()
if config_app.get("ultima_carpeta"): # type: ignore
    ruta_destino.set(config_app["ultima_carpeta"]) # type: ignore

# Lista de opciones de calidad disponibles para el video actual
opciones_calidad: list[str] = []

# Variable para la calidad seleccionada en el combobox
calidad_seleccionada = ctk.StringVar()

# Variable booleana para modo solo audio
solo_audio = ctk.BooleanVar()
solo_audio.set(config_app.get("solo_audio_por_defecto", False)) # type: ignore

# Diccionario con información completa del video obtenida de yt-dlp
info_video = {}

# ID del mejor formato de video disponible (mayor resolución)
mejor_itag: str = ""

# Variables para el progreso
progreso_actual = ctk.DoubleVar()
velocidad_descarga = ctk.StringVar(value="0 MB/s")
tiempo_restante = ctk.StringVar(value="--:--")
bytes_descargados = ctk.StringVar(value="0 / 0 MB")

# Variable para controlar el log periódico (evitar duplicados)
ultimo_porcentaje_log = 0

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================

def seleccionar_carpeta():
    """
    Abre un diálogo para seleccionar la carpeta de destino de las descargas.
    
    Actualiza la variable global 'ruta_destino' con la carpeta seleccionada.
    Si el usuario cancela la selección, no se modifica la variable.
    También guarda la selección en la configuración.
    """
    carpeta = filedialog.askdirectory(initialdir=ruta_destino.get())
    if carpeta:
        ruta_destino.set(carpeta)
        # Guardar en configuración
        config_app["ultima_carpeta"] = carpeta
        guardar_configuracion(config_app)

def obtener_info():
    """
    Obtiene información detallada del video de YouTube desde la URL proporcionada.
    Usa caché para evitar consultas repetidas y ThreadPoolExecutor para no bloquear la UI.
    
    Proceso:
    1. Valida que se haya ingresado una URL válida de YouTube
    2. Verifica conectividad con YouTube
    3. Busca en caché primero
    4. Extrae información del video usando yt-dlp (si no está en caché)
    5. Procesa los formatos disponibles según el modo (video/audio)
    6. Actualiza la interfaz con la información obtenida
    7. Determina el mejor formato de video disponible
    
    Variables globales modificadas:
    - info_video: información completa del video
    - opciones_calidad: lista de formatos disponibles
    - mejor_itag: ID del mejor formato de video
    - cache_videos: caché de información
    
    Excepciones:
    - Muestra error si la URL es inválida o no se puede acceder al video
    - Maneja errores de conexión y formatos no disponibles
    """
    global mejor_itag
    url = entrada_url.get().strip()
    
    # Validar que se haya ingresado una URL
    if not url:
        messagebox.showwarning("URL requerida", "Por favor ingresa un enlace de YouTube.")
        return
    
    # Validar que sea una URL de YouTube
    if not validar_url_youtube(url):
        messagebox.showwarning("URL inválida", "Por favor ingresa una URL válida de YouTube.\n\nFormatos aceptados:\n- youtube.com/watch?v=...\n- youtu.be/...\n- youtube.com/shorts/...")
        return
    
    # Verificar conectividad
    if not verificar_conectividad(url):
        messagebox.showerror("Sin conexión", "No se puede conectar a YouTube.\nVerifica tu conexión a Internet.")
        return
    
    # Verificar que ffmpeg esté disponible
    if not FFMPEG_PATH or not os.path.exists(FFMPEG_PATH):
        respuesta = messagebox.askyesno("FFmpeg no encontrado", 
                             "FFmpeg no se encontró en el sistema.\nAlgunas funciones pueden no estar disponibles.\n\n¿Continuar de todos modos?")
        if not respuesta:
            return
    
    def tarea_info():
        """Función interna para ejecutar la obtención de info en hilo separado con caché."""
        progreso_barra_info = None  # Inicializar variable
        try:
            # Verificar caché primero
            if url in cache_videos:
                agregar_log(f"📦 Usando información desde caché", "INFO")
                video_info = cache_videos[url]
            else:
                # Mostrar progreso
                progreso_barra_info = ctk.CTkProgressBar(frame_info, mode='indeterminate')
                progreso_barra_info.pack(pady=5)
                progreso_barra_info.start()
                boton_info.configure(state="disabled")
                
                agregar_log("🔍 Obteniendo información del video...", "INFO")
                
                # Configurar yt-dlp para extraer información sin descargar
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    # Extraer información del video
                    video_info = ydl.extract_info(url, download=False) # type: ignore
                    
                    # Guardar en caché
                    cache_videos[url] = video_info # type: ignore
                
                # Detener animación ANTES de destruir
                if progreso_barra_info:
                    progreso_barra_info.stop()
                    ventana.update()  # Procesar eventos pendientes
                    progreso_barra_info.destroy()
                boton_info.configure(state="normal")
            
            # Actualizar información global del video
            info_video.clear()
            info_video.update(video_info) # type: ignore

            # Extraer datos básicos del video
            titulo = video_info.get("title", "Sin título") # type: ignore
            duracion = video_info.get("duration_string", "Desconocida") # type: ignore
            formatos = video_info.get("formats") # type: ignore

            agregar_log(f"📹 Video encontrado: {titulo}", "SUCCESS")

            # Inicializar variables para procesamiento de formatos
            opciones: list[str] = []
            global mejor_itag
            mejor_video: dict[str, Any] | None = None

            # Validar que existan formatos disponibles
            if not formatos:
                messagebox.showerror("Error", "No se encontraron formatos disponibles para este video.")
                return

            # Procesar formatos disponibles según el modo seleccionado
            for f in formatos:  # type: ignore
                if solo_audio.get():
                    # Modo solo audio: buscar formatos de audio sin video
                    if f.get("acodec") != "none" and f.get("vcodec") == "none": # type: ignore
                        kbps = f.get("abr", '?')# type: ignore
                        ext = f.get("ext")# type: ignore
                        filesize = f.get("filesize", 0)  # type: ignore
                        size_mb = f"{filesize // (1024*1024)}MB" if filesize else "?"
                        opciones.append(f"Audio {kbps}kbps - {ext} ({size_mb}) - itag:{f['format_id']}")
                else:
                    # Modo video: buscar formatos con video SOLO MP4 (no webm)
                    if f.get("vcodec") != "none" and f.get("ext") == "mp4": # type: ignore
                        res = f.get("height", 0)    # type: ignore
                        fps = f.get("fps", '?')# type: ignore
                        ext = f.get("ext")# type: ignore
                        itag = f['format_id']# type: ignore
                        filesize = f.get("filesize", 0)  # type: ignore
                        size_mb = f"{filesize // (1024*1024)}MB" if filesize else "?"
                        opciones.append(f"Video {res}p {fps}fps - {ext} ({size_mb}) - itag:{itag}")
                        
                        # Determinar el mejor formato (mayor resolución)
                        if mejor_video is None or int(res) > int(mejor_video.get("height", 0)): # type: ignore
                            mejor_video = f # type: ignore

            # Ordenar opciones por calidad (descendente) y eliminar duplicados
            opciones = sorted(set(opciones), reverse=True)

            # Actualizar interfaz con las opciones disponibles
            opciones_calidad.clear()
            opciones_calidad.extend(opciones)
            calidad_combo.configure(values=opciones_calidad)
            if opciones:
                calidad_combo.set(opciones_calidad[0])

            # Guardar el itag del mejor video
            if mejor_video:
                mejor_itag = mejor_video['format_id'] # type: ignore

            # Mostrar información del video en la interfaz
            uploader = str(video_info.get('uploader', 'Desconocido')) if video_info else 'Desconocido' # type: ignore
            view_count = video_info.get('view_count', 0) # type: ignore
            views = f"{view_count:,}" if view_count else "Desconocido"
            
            info_text = f"📹 {titulo}\n⏱️ {duracion} | 👤 {uploader}\n👁️ {views} visualizaciones"
            etiqueta_info.configure(text=info_text)
            
            agregar_log(f"✅ Información cargada: {len(opciones)} formatos disponibles", "SUCCESS")
            messagebox.showinfo("Info obtenida", f"✅ Video: {titulo}\n📊 {len(opciones)} formatos disponibles")
            
        except Exception as e:
            agregar_log(f"❌ Error al obtener información: {str(e)}", "ERROR")
            messagebox.showerror("Error al obtener info", f"❌ {str(e)}")
            logging.error(f"Error en obtener_info: {e}")
        finally:
            # Restaurar interfaz - limpiar barra de progreso si existe
            if progreso_barra_info is not None:
                try:
                    progreso_barra_info.stop()
                    ventana.update()
                    progreso_barra_info.destroy()
                except Exception as e:
                    logging.error(f"Error al destruir barra de progreso: {e}")
            boton_info.configure(state="normal")

    # Ejecutar en ThreadPoolExecutor en lugar de threading manual
    executor.submit(tarea_info)

def descargar():
    """
    Inicia el proceso de descarga del video/audio seleccionado.
    
    Proceso:
    1. Valida que todos los campos requeridos estén completos
    2. Extrae el itag del formato seleccionado
    3. Ejecuta la descarga usando ThreadPoolExecutor
    4. Configura yt-dlp con las opciones apropiadas
    5. Maneja la conversión a MP3 si está en modo solo audio
    
    Validaciones:
    - URL debe estar presente y ser válida
    - Carpeta de destino debe estar seleccionada
    - Calidad debe estar seleccionada
    - FFmpeg debe estar disponible para conversión de audio
    
    Threading:
    - La descarga se ejecuta con ThreadPoolExecutor
    - La interfaz permanece responsiva durante la descarga
    - Se muestra progreso real de la descarga
    - Permite múltiples descargas simultáneas
    """
    url = entrada_url.get().strip()
    carpeta = ruta_destino.get().strip()
    calidad = calidad_combo.get()
    
    # Validar campos requeridos
    if not url or not carpeta:
        messagebox.showwarning("Campos requeridos", "Por favor completa todos los campos.")
        return

    if not calidad:
        messagebox.showwarning("Calidad requerida", "Selecciona una calidad para continuar.")
        return
    
    # Validar URL de YouTube con validación mejorada
    if not validar_url_youtube(url):
        messagebox.showwarning("URL inválida", "Por favor ingresa una URL válida de YouTube.\n\nFormatos aceptados:\n- youtube.com/watch?v=...\n- youtu.be/...\n- youtube.com/shorts/...")
        return
    
    # Validar que la carpeta existe
    if not os.path.exists(carpeta):
        messagebox.showerror("Error", "La carpeta de destino no existe.")
        return
    
    # Verificar ffmpeg
    if not FFMPEG_PATH:
        respuesta = messagebox.askyesno("FFmpeg no encontrado", 
                                      "FFmpeg no se encontró. ¿Continuar de todos modos? (Puede fallar)")
        if not respuesta:
            return

    # Extraer itag de la selección de calidad
    try:
        itag = calidad.split("itag:")[-1]
    except:
        messagebox.showerror("Error", "No se pudo leer el formato seleccionado.")
        return

    def tarea():
        """
        Función interna que ejecuta la descarga en un hilo separado.
        
        Configuraciones de yt-dlp:
        - ffmpeg_location: ruta al ejecutable de ffmpeg
        - format: formato específico a descargar
        - outtmpl: plantilla para el nombre del archivo de salida
        - merge_output_format: formato final del archivo
        - progress_hooks: función callback para el progreso
        - postprocessors: procesadores post-descarga (conversión a MP3)
        
        Estados de la interfaz:
        - Deshabilita el botón de descarga durante el proceso
        - Muestra progreso real de la descarga
        - Restaura el estado normal al finalizar
        """
        global ultimo_porcentaje_log
        
        try:
            # Resetear contador de log al inicio
            ultimo_porcentaje_log = 0
            
            # Deshabilitar botón y resetear progreso
            boton_descargar.configure(state="disabled")
            progreso_actual.set(0)
            velocidad_descarga.set("0 MB/s")
            tiempo_restante.set("--:--")
            bytes_descargados.set("0 / 0 MB")
            
            agregar_log("🚀 Iniciando descarga...", "INFO")

            # Determinar extensión según el modo
            extension = "mp3" if solo_audio.get() else "mp4"

            # Configurar opciones de yt-dlp
            opciones: dict[str, Any] = {
                'format': f"{itag}+bestaudio/best",  # Formato específico + mejor audio
                'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),  # Plantilla de nombre
                'merge_output_format': extension,  # Formato de salida final
                'progress_hooks': [progreso_hook],  # Hook para progreso
                'quiet': False,
                'no_warnings': False,
                # Post-procesador para conversión a MP3 (solo en modo audio)
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }] if solo_audio.get() else []
            }
            
            # Añadir ffmpeg_location solo si está disponible
            if FFMPEG_PATH:
                opciones['ffmpeg_location'] = FFMPEG_PATH

            # Ejecutar descarga con yt-dlp
            with yt_dlp.YoutubeDL(opciones) as ydl: # type: ignore
                ydl.download([url])  # type: ignore
            
            agregar_log("✅ Descarga completada correctamente", "SUCCESS")
            messagebox.showinfo("Completado", f"✅ Descarga completada correctamente\n\n📁 {carpeta}")
            
            # Log de finalización
            logging.info(f"Descarga completada: {url}")
            
        except Exception as e:
            agregar_log(f"❌ Error durante la descarga: {str(e)}", "ERROR")
            messagebox.showerror("Error de descarga", f"❌ {str(e)}\n\nRevisa el log para más detalles.")
            logging.error(f"Error en descarga: {e}")
        finally:
            # Restaurar estado de la interfaz
            boton_descargar.configure(state="normal")
            progreso_actual.set(0)

    # Ejecutar descarga con ThreadPoolExecutor
    executor.submit(tarea)

def progreso_hook(d: dict[str, Any]):
    """
    Función callback llamada por yt-dlp durante el progreso de descarga.
    
    Parámetros:
    - d: diccionario con información del progreso de descarga
         Claves importantes: 'status', 'downloaded_bytes', 'total_bytes', 'speed', 'eta'
    
    Estados posibles:
    - 'downloading': descarga en progreso
    - 'finished': descarga completada
    - 'error': error durante la descarga
    
    Funcionalidad:
    - Actualiza la barra de progreso real
    - Muestra velocidad de descarga
    - Muestra tiempo estimado restante
    - Muestra bytes descargados vs total
    - Mantiene log de actividad
    """
    global ultimo_porcentaje_log
    
    if d['status'] == 'downloading':
        try:
            # Obtener datos del progreso
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            filename = d.get('filename', '')
            
            # Actualizar barra de progreso
            if total > 0:
                porcentaje = (downloaded / total) * 100
                progreso_actual.set(porcentaje)
            
            # Actualizar velocidad
            if speed:
                if speed >= 1024 * 1024:  # MB/s
                    velocidad_descarga.set(f"{speed / (1024 * 1024):.2f} MB/s")
                else:  # KB/s
                    velocidad_descarga.set(f"{speed / 1024:.2f} KB/s")
            
            # Actualizar tiempo restante
            if eta:
                minutos = eta // 60
                segundos = eta % 60
                tiempo_restante.set(f"{int(minutos):02d}:{int(segundos):02d}")
            
            # Actualizar bytes descargados
            downloaded_mb = downloaded / (1024 * 1024)
            total_mb = total / (1024 * 1024) if total > 0 else 0
            bytes_descargados.set(f"{downloaded_mb:.1f} / {total_mb:.1f} MB")
            
            # Log periódico (cada 10% - sin duplicados)
            if total > 0:  # type: ignore
                porcentaje_int = int(porcentaje)  # type: ignore
                if porcentaje_int % 10 == 0 and porcentaje_int > 0 and porcentaje_int != ultimo_porcentaje_log:
                    ultimo_porcentaje_log = porcentaje_int
                    filename_short = os.path.basename(filename) if filename else "archivo"
                    agregar_log(f"📥 Descargando {filename_short}: {porcentaje:.1f}% - {velocidad_descarga.get()}", "INFO")   # type: ignore
            
        except Exception as e:
            logging.error(f"Error en progreso_hook: {e}")
    
    elif d['status'] == 'finished':
        # Resetear contador de log
        ultimo_porcentaje_log = 0
        filename = os.path.basename(d.get('filename', ''))
        agregar_log(f"🎉 Descarga terminada: {filename}", "SUCCESS")
        progreso_actual.set(100)
    
    elif d['status'] == 'error':
        agregar_log(f"❌ Error en descarga: {d.get('error', 'Error desconocido')}", "ERROR")
    
    # Actualizar interfaz
    ventana.update_idletasks()

def agregar_log(mensaje: str, tipo: str = "INFO"):
    """
    Añade un mensaje al log de la interfaz.
    
    Args:
        mensaje: Mensaje a mostrar
        tipo: Tipo de mensaje (INFO, SUCCESS, ERROR, WARNING)
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    colores = {
        "INFO": "black",
        "SUCCESS": "green", 
        "ERROR": "red",
        "WARNING": "orange"
    }
    
    # Añadir al widget de texto
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
    
    # Aplicar color según el tipo
    if tipo in colores:
        start_line = log_text.index(tk.END + "-2l linestart")
        end_line = log_text.index(tk.END + "-2l lineend")
        log_text.tag_add(tipo, start_line, end_line)
        log_text.tag_config(tipo, foreground=colores[tipo])
    
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)  # Scroll automático

def limpiar_log():
    """Limpia el log de actividad."""
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.config(state=tk.DISABLED)
    agregar_log("📋 Log limpiado", "INFO")

def on_solo_audio_change():
    """Callback cuando cambia el estado del checkbox de solo audio."""
    # Limpiar opciones cuando cambia el modo
    opciones_calidad.clear()
    calidad_combo.configure(values=[])
    calidad_seleccionada.set("")
    
    # Guardar preferencia
    config_app["solo_audio_por_defecto"] = solo_audio.get()
    guardar_configuracion(config_app)

def on_closing():
    """Función llamada al cerrar la aplicación."""
    # Guardar configuración de ventana
    config_app["ventana_ancho"] = ventana.winfo_width()
    config_app["ventana_alto"] = ventana.winfo_height()
    guardar_configuracion(config_app)
    
    # Cerrar aplicación
    ventana.destroy()

def cambiar_tema():
    """Cambia entre tema oscuro y claro."""
    tema_actual = ctk.get_appearance_mode()
    if tema_actual == "Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

# =============================================================================
# CREACIÓN DE ELEMENTOS GRÁFICOS
# =============================================================================

# Frame principal
frame_principal = ctk.CTkFrame(ventana)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame para URL y botón info
frame_url = ctk.CTkFrame(frame_principal)
frame_url.pack(fill=tk.X, pady=(0, 10))

ctk.CTkLabel(frame_url, text="URL de YouTube:", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=5, pady=5)

# Campo de entrada para la URL del video
entrada_url = ctk.CTkEntry(frame_url, width=500, height=35, font=("Arial", 11))
entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

# Botón para obtener información del video
boton_info = ctk.CTkButton(frame_url, text="Obtener Info", command=obtener_info, 
                      width=120, height=35, font=("Arial", 11, "bold"))
boton_info.pack(side=tk.RIGHT, padx=5)

# Botón para cambiar tema
boton_tema = ctk.CTkButton(frame_url, text="🌓", command=cambiar_tema, 
                      width=40, height=35, font=("Arial", 14))
boton_tema.pack(side=tk.RIGHT, padx=5)

# Frame para información del video
frame_info = ctk.CTkFrame(frame_principal)
frame_info.pack(fill=tk.X, pady=(0, 10))

# Etiqueta para mostrar información del video
etiqueta_info = ctk.CTkLabel(frame_info, text="", justify="left", 
                        font=("Arial", 10), anchor="w")
etiqueta_info.pack(fill=tk.X, padx=10, pady=10)

# Frame para opciones
frame_opciones = ctk.CTkFrame(frame_principal)
frame_opciones.pack(fill=tk.X, pady=(0, 10))

# Checkbox para modo solo audio
chk_audio = ctk.CTkCheckBox(frame_opciones, text="Solo audio (MP3)", 
                          variable=solo_audio, command=on_solo_audio_change,
                          font=("Arial", 11))
chk_audio.pack(anchor=tk.W, padx=10, pady=5)

# Label y combobox para calidad
ctk.CTkLabel(frame_opciones, text="Calidad:", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 0))
calidad_combo = ctk.CTkComboBox(frame_opciones, variable=calidad_seleccionada, 
                            width=660, height=35, font=("Arial", 10), 
                            values=[], state="readonly")
calidad_combo.pack(fill=tk.X, padx=10, pady=(5, 10))

# Frame para carpeta destino
frame_carpeta = ctk.CTkFrame(frame_principal)
frame_carpeta.pack(fill=tk.X, pady=(10, 0))

ctk.CTkLabel(frame_carpeta, text="Carpeta de destino:", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=10, pady=5)

# Botón y etiqueta para carpeta
frame_carpeta_sel = ctk.CTkFrame(frame_carpeta, fg_color="transparent")
frame_carpeta_sel.pack(fill=tk.X, pady=(5, 10), padx=10)

btn_carpeta = ctk.CTkButton(frame_carpeta_sel, text="📁 Seleccionar Carpeta", 
                       command=seleccionar_carpeta, width=180, height=35,
                       font=("Arial", 11, "bold"))
btn_carpeta.pack(side=tk.LEFT)

etiqueta_carpeta = ctk.CTkLabel(frame_carpeta_sel, textvariable=ruta_destino, 
                           font=("Arial", 10), text_color="#3b8ed0")
etiqueta_carpeta.pack(side=tk.LEFT, padx=(10, 0))

# Frame para progreso
frame_progreso = ctk.CTkFrame(frame_principal)
frame_progreso.pack(fill=tk.X, pady=(15, 0))

ctk.CTkLabel(frame_progreso, text="Progreso de descarga:", font=("Arial", 11, "bold")).pack(anchor=tk.W, padx=10, pady=5)

# Barra de progreso real
progreso_barra = ctk.CTkProgressBar(frame_progreso, variable=progreso_actual, 
                                width=640, height=20)
progreso_barra.pack(fill=tk.X, pady=(5, 10), padx=10)

# Frame para estadísticas
frame_stats = ctk.CTkFrame(frame_progreso, fg_color="transparent")
frame_stats.pack(fill=tk.X, padx=10)

# Estadísticas de descarga
ctk.CTkLabel(frame_stats, text="Velocidad:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5)
ctk.CTkLabel(frame_stats, textvariable=velocidad_descarga, font=("Arial", 10), text_color="#3b8ed0").grid(row=0, column=1, sticky=tk.W, padx=(5, 20))

ctk.CTkLabel(frame_stats, text="Tiempo restante:", font=("Arial", 10)).grid(row=0, column=2, sticky=tk.W, padx=5)
ctk.CTkLabel(frame_stats, textvariable=tiempo_restante, font=("Arial", 10), text_color="#3b8ed0").grid(row=0, column=3, sticky=tk.W, padx=(5, 20))

ctk.CTkLabel(frame_stats, text="Descargado:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, padx=5, pady=(5,0))
ctk.CTkLabel(frame_stats, textvariable=bytes_descargados, font=("Arial", 10), text_color="#3b8ed0").grid(row=1, column=1, sticky=tk.W, padx=(5, 20), pady=(5,0))

# Botón de descarga
boton_descargar = ctk.CTkButton(frame_principal, text="🚀 DESCARGAR", command=descargar, 
                           width=200, height=45, font=("Arial", 14, "bold"))
boton_descargar.pack(pady=(15, 10))

# Frame para log
frame_log = ctk.CTkFrame(frame_principal)
frame_log.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

# Label y botones para log
frame_log_header = ctk.CTkFrame(frame_log, fg_color="transparent")
frame_log_header.pack(fill=tk.X, padx=10, pady=(5,0))

ctk.CTkLabel(frame_log_header, text="Log de actividad:", font=("Arial", 11, "bold")).pack(side=tk.LEFT)

btn_limpiar_log = ctk.CTkButton(frame_log_header, text="Limpiar Log", command=limpiar_log,
                           width=100, height=28, font=("Arial", 10))
btn_limpiar_log.pack(side=tk.RIGHT)

# Widget de texto con scroll para el log
log_text = scrolledtext.ScrolledText(frame_log, height=8, font=("Consolas", 9),
                                   state=tk.DISABLED, wrap=tk.WORD, bg="#2b2b2b", fg="#ffffff")
log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10), padx=10)

# =============================================================================
# INICIALIZACIÓN Y EJECUCIÓN PRINCIPAL
# =============================================================================

# Configurar protocolo de cierre
ventana.protocol("WM_DELETE_WINDOW", on_closing)

# Verificar ffmpeg al inicio
if FFMPEG_PATH:
    agregar_log(f"✅ FFmpeg encontrado en: {FFMPEG_PATH}", "SUCCESS")
else:
    agregar_log("⚠️ FFmpeg no encontrado. Instala FFmpeg para mejor compatibilidad.", "WARNING")

# Mensaje de bienvenida
agregar_log("🎬 Descargador de YouTube v2.0 - Modern UI - by HanserlodXP", "INFO")
agregar_log("📝 Ingresa una URL de YouTube y presiona 'Obtener Info' para comenzar", "INFO")

# Log de configuración cargada
if config_app.get("ultima_carpeta"):   # type: ignore
    agregar_log(f"📁 Carpeta por defecto: {config_app['ultima_carpeta']}", "INFO")

# Iniciar el bucle principal de la interfaz gráfica
# Esta línea mantiene la ventana abierta y responsiva a los eventos del usuario
ventana.mainloop()