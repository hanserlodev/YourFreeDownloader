"""
Descargador de YouTube con interfaz gráfica - Versión Mejorada
============================================================

Este módulo implementa una aplicación de escritorio para descargar videos y audio
de YouTube utilizando tkinter para la interfaz gráfica y yt-dlp para el procesamiento
de descargas.

Características:
- Descarga de videos en diferentes calidades
- Extracción de solo audio en formato MP3
- Interfaz gráfica intuitiva
- Barra de progreso real durante la descarga
- Selección de carpeta de destino
- Log de descarga en tiempo real
- Detección automática de ffmpeg
- Validación de URLs de YouTube
- Manejo mejorado de errores
- Guardar/cargar configuración

Dependencias:
- tkinter (incluido en Python estándar)
- yt-dlp: pip install yt-dlp
- ffmpeg: debe estar instalado en el sistema

Autor: HanserlodXP
Fecha: 02/09/2025
Versión: 1.1
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import threading
import yt_dlp # type: ignore
from typing import Any, Optional
import re
import json
import shutil
import logging
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================

def encontrar_ffmpeg() -> Optional[str]:
    """
    Busca automáticamente la ubicación de ffmpeg en el sistema.
    
    Returns:
        str | None: Ruta a ffmpeg si se encuentra, None en caso contrario
    
    Proceso:
    1. Busca ffmpeg en el PATH del sistema
    2. Verifica rutas comunes según el sistema operativo
    3. Retorna la primera ruta válida encontrada
    """
    # Buscar ffmpeg en el PATH del sistema
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Rutas comunes en diferentes sistemas operativos
    rutas_comunes = [
        r"C:\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe",  # Windows personalizado
        r"C:\ffmpeg\bin\ffmpeg.exe",  # Windows estándar
        "/usr/bin/ffmpeg",  # Linux/Mac
        "/usr/local/bin/ffmpeg",  # Linux/Mac alternativo
        "ffmpeg"  # Fallback
    ]
    
    for ruta in rutas_comunes:
        if os.path.exists(ruta):
            return ruta
    
    return None

# Detectar ffmpeg automáticamente
FFMPEG_PATH = encontrar_ffmpeg()

def validar_url_youtube(url: str) -> bool:
    """
    Valida si una URL pertenece a YouTube.
    
    Args:
        url: URL a validar
    
    Returns:
        bool: True si es una URL válida de YouTube
    """
    patron = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return re.match(patron, url) is not None

def cargar_configuracion() -> dict: # type: ignore
    """
    Carga la configuración desde archivo config.json.
    
    Returns:
        dict: Configuración cargada o configuración por defecto
    """
    try:
        with open("config.json", "r", encoding="utf-8") as f:
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
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar configuración: {e}")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('descargador.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Cargar configuración inicial
config_app = cargar_configuracion() # type: ignore

# =============================================================================
# INICIALIZACIÓN DE LA INTERFAZ
# =============================================================================

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Descargador de YouTube v1.1 - by HanserlodXP")
ventana.geometry(f"{config_app.get('ventana_ancho', 700)}x{config_app.get('ventana_alto', 600)}") # type: ignore

# =============================================================================
# VARIABLES GLOBALES DE ESTADO
# =============================================================================

# Variable para almacenar la ruta de destino seleccionada
ruta_destino = tk.StringVar()
if config_app.get("ultima_carpeta"): # type: ignore
    ruta_destino.set(config_app["ultima_carpeta"]) # type: ignore

# Lista de opciones de calidad disponibles para el video actual
opciones_calidad: list[str] = []

# Variable para la calidad seleccionada en el combobox
calidad_seleccionada = tk.StringVar()

# Variable booleana para modo solo audio
solo_audio = tk.BooleanVar()
solo_audio.set(config_app.get("solo_audio_por_defecto", False)) # type: ignore

# Diccionario con información completa del video obtenida de yt-dlp
info_video = {}

# ID del mejor formato de video disponible (mayor resolución)
mejor_itag: str = ""

# Variables para el progreso
progreso_actual = tk.DoubleVar()
velocidad_descarga = tk.StringVar(value="0 MB/s")
tiempo_restante = tk.StringVar(value="--:--")
bytes_descargados = tk.StringVar(value="0 / 0 MB")

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
    
    Proceso:
    1. Valida que se haya ingresado una URL válida de YouTube
    2. Extrae información del video usando yt-dlp
    3. Procesa los formatos disponibles según el modo (video/audio)
    4. Actualiza la interfaz con la información obtenida
    5. Determina el mejor formato de video disponible
    
    Variables globales modificadas:
    - info_video: información completa del video
    - opciones_calidad: lista de formatos disponibles
    - mejor_itag: ID del mejor formato de video
    
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
        messagebox.showwarning("URL inválida", "Por favor ingresa una URL válida de YouTube.")
        return
    
    # Verificar que ffmpeg esté disponible
    if not FFMPEG_PATH or not os.path.exists(FFMPEG_PATH):
        messagebox.showwarning("FFmpeg no encontrado", 
                             "FFmpeg no se encontró en el sistema. Algunas funciones pueden no estar disponibles.")
    
    def tarea_info():
        """Función interna para ejecutar la obtención de info en hilo separado."""
        try:
            # Mostrar progreso
            progreso_barra_info = ttk.Progressbar(frame_info, mode='indeterminate')
            progreso_barra_info.pack(pady=5)
            progreso_barra_info.start()
            boton_info.config(state="disabled")
            
            agregar_log("🔍 Obteniendo información del video...", "INFO")
            
            # Configurar yt-dlp para extraer información sin descargar
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                # Extraer información del video
                video_info = ydl.extract_info(url, download=False) # type: ignore
                
                # Actualizar información global del video
                info_video.clear()
                info_video.update(video_info) # type: ignore

                # Extraer datos básicos del video
                titulo = video_info.get("title") # type: ignore
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
                        # Modo video: buscar formatos con video
                        if f.get("vcodec") != "none": # type: ignore
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
                calidad_combo["values"] = opciones_calidad
                if opciones:
                    calidad_combo.current(0)

                # Guardar el itag del mejor video
                if mejor_video:
                    mejor_itag = mejor_video['format_id'] # type: ignore

                # Mostrar información del video en la interfaz
                uploader = str(video_info['uploader']) if video_info and 'uploader' in video_info else 'Desconocido' # type: ignore
                view_count = video_info.get('view_count', 0) # type: ignore
                views = f"{view_count:,}" if view_count else "Desconocido"
                
                info_text = f"Título: {titulo}\nDuración: {duracion}\nAutor: {uploader}\nVistas: {views}"
                etiqueta_info.config(text=info_text)
                
                agregar_log(f"✅ Información cargada: {len(opciones)} formatos disponibles", "SUCCESS")
                messagebox.showinfo("Info obtenida", "Información del video cargada correctamente.")
                
        except Exception as e:
            agregar_log(f"❌ Error al obtener información: {str(e)}", "ERROR")
            messagebox.showerror("Error al obtener info", str(e))
            logging.error(f"Error en obtener_info: {e}")
        finally:
            # Restaurar interfaz
            progreso_barra_info.destroy()  # type: ignore
            boton_info.config(state="normal")

    # Ejecutar en hilo separado
    threading.Thread(target=tarea_info, daemon=True).start()

def descargar():
    """
    Inicia el proceso de descarga del video/audio seleccionado.
    
    Proceso:
    1. Valida que todos los campos requeridos estén completos
    2. Extrae el itag del formato seleccionado
    3. Ejecuta la descarga en un hilo separado para no bloquear la interfaz
    4. Configura yt-dlp con las opciones apropiadas
    5. Maneja la conversión a MP3 si está en modo solo audio
    
    Validaciones:
    - URL debe estar presente y ser válida
    - Carpeta de destino debe estar seleccionada
    - Calidad debe estar seleccionada
    - FFmpeg debe estar disponible
    
    Threading:
    - La descarga se ejecuta en un hilo separado
    - La interfaz permanece responsiva durante la descarga
    - Se muestra progreso real de la descarga
    """
    global ultimo_porcentaje_log, ultima_linea_progreso
    
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
    
    # Validar URL de YouTube
    if not validar_url_youtube(url):
        messagebox.showwarning("URL inválida", "Por favor ingresa una URL válida de YouTube.")
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
        try:
            # Reset variables de control de log
            ultimo_porcentaje_log = 0  # type: ignore
            ultima_linea_progreso = None   # type: ignore
            
            # Deshabilitar botón y resetear progreso
            boton_descargar.config(state="disabled")
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
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])  # type: ignore
            
            agregar_log("✅ Descarga completada correctamente", "SUCCESS")
            messagebox.showinfo("Completado", "✅ Descarga completada correctamente.")
            
            # Log de finalización
            logging.info(f"Descarga completada: {url}")
            
        except Exception as e:
            agregar_log(f"❌ Error durante la descarga: {str(e)}", "ERROR")
            messagebox.showerror("Error de descarga", str(e))
            logging.error(f"Error en descarga: {e}")
        finally:
            # Restaurar estado de la interfaz
            boton_descargar.config(state="normal")
            progreso_actual.set(0)
            
            # Reset variables de control
            ultimo_porcentaje_log = 0   # type: ignore
            ultima_linea_progreso = None   # type: ignore

    # Ejecutar descarga en hilo separado
    threading.Thread(target=tarea, daemon=True).start()

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
            
            # Log periódico (cada 10%)
            if total > 0 and int(porcentaje) % 10 == 0 and int(porcentaje) > 0:  # type: ignore
                filename_short = os.path.basename(filename) if filename else "archivo"
                agregar_log(f"📥 Descargando {filename_short}: {porcentaje:.1f}% - {velocidad_descarga.get()}", "INFO")   # type: ignore
            
        except Exception as e:
            logging.error(f"Error en progreso_hook: {e}")
    
    elif d['status'] == 'finished':
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
    calidad_combo["values"] = []
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

# =============================================================================
# CREACIÓN DE ELEMENTOS GRÁFICOS
# =============================================================================

# Frame principal
frame_principal = tk.Frame(ventana)
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Frame para URL y botón info
frame_url = tk.Frame(frame_principal)
frame_url.pack(fill=tk.X, pady=(0, 10))

tk.Label(frame_url, text="URL de YouTube:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

# Campo de entrada para la URL del video
entrada_url = tk.Entry(frame_url, width=70, font=("Arial", 10))
entrada_url.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

# Botón para obtener información del video
boton_info = tk.Button(frame_url, text="Obtener Info", command=obtener_info, 
                      bg="#4CAF50", fg="white", font=("Arial", 9, "bold"))
boton_info.pack(side=tk.RIGHT)

# Frame para información del video
frame_info = tk.Frame(frame_principal)
frame_info.pack(fill=tk.X, pady=(0, 10))

# Etiqueta para mostrar información del video
etiqueta_info = tk.Label(frame_info, text="", justify="left", 
                        font=("Arial", 9), bg="#f0f0f0", relief=tk.RIDGE, 
                        padx=10, pady=10)
etiqueta_info.pack(fill=tk.X)

# Frame para opciones
frame_opciones = tk.Frame(frame_principal)
frame_opciones.pack(fill=tk.X, pady=(0, 10))

# Checkbox para modo solo audio
chk_audio = tk.Checkbutton(frame_opciones, text="Solo audio (MP3)", 
                          variable=solo_audio, command=on_solo_audio_change,
                          font=("Arial", 10))
chk_audio.pack(anchor=tk.W)

# Label y combobox para calidad
tk.Label(frame_opciones, text="Calidad:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 0))
calidad_combo = ttk.Combobox(frame_opciones, textvariable=calidad_seleccionada, 
                            width=80, font=("Arial", 9))
calidad_combo.pack(fill=tk.X, pady=(5, 0))

# Frame para carpeta destino
frame_carpeta = tk.Frame(frame_principal)
frame_carpeta.pack(fill=tk.X, pady=(10, 0))

tk.Label(frame_carpeta, text="Carpeta de destino:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

# Botón y etiqueta para carpeta
frame_carpeta_sel = tk.Frame(frame_carpeta)
frame_carpeta_sel.pack(fill=tk.X, pady=(5, 0))

btn_carpeta = tk.Button(frame_carpeta_sel, text="Seleccionar Carpeta", 
                       command=seleccionar_carpeta, bg="#2196F3", fg="white",
                       font=("Arial", 9, "bold"))
btn_carpeta.pack(side=tk.LEFT)

etiqueta_carpeta = tk.Label(frame_carpeta_sel, textvariable=ruta_destino, 
                           font=("Arial", 9), fg="blue")
etiqueta_carpeta.pack(side=tk.LEFT, padx=(10, 0))

# Frame para progreso
frame_progreso = tk.Frame(frame_principal)
frame_progreso.pack(fill=tk.X, pady=(15, 0))

tk.Label(frame_progreso, text="Progreso de descarga:", font=("Arial", 10, "bold")).pack(anchor=tk.W)

# Barra de progreso real
progreso_barra = ttk.Progressbar(frame_progreso, variable=progreso_actual, 
                                maximum=100, length=400)
progreso_barra.pack(fill=tk.X, pady=(5, 10))

# Frame para estadísticas
frame_stats = tk.Frame(frame_progreso)
frame_stats.pack(fill=tk.X)

# Estadísticas de descarga
tk.Label(frame_stats, text="Velocidad:", font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W)
tk.Label(frame_stats, textvariable=velocidad_descarga, font=("Arial", 9), fg="blue").grid(row=0, column=1, sticky=tk.W, padx=(5, 20))

tk.Label(frame_stats, text="Tiempo restante:", font=("Arial", 9)).grid(row=0, column=2, sticky=tk.W)
tk.Label(frame_stats, textvariable=tiempo_restante, font=("Arial", 9), fg="blue").grid(row=0, column=3, sticky=tk.W, padx=(5, 20))

tk.Label(frame_stats, text="Descargado:", font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W)
tk.Label(frame_stats, textvariable=bytes_descargados, font=("Arial", 9), fg="blue").grid(row=1, column=1, sticky=tk.W, padx=(5, 20))

# Botón de descarga
boton_descargar = tk.Button(frame_principal, text="🚀 DESCARGAR", command=descargar, 
                           bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                           height=2)
boton_descargar.pack(pady=(15, 10))

# Frame para log
frame_log = tk.Frame(frame_principal)
frame_log.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

# Label y botones para log
frame_log_header = tk.Frame(frame_log)
frame_log_header.pack(fill=tk.X)

tk.Label(frame_log_header, text="Log de actividad:", font=("Arial", 10, "bold")).pack(side=tk.LEFT)

btn_limpiar_log = tk.Button(frame_log_header, text="Limpiar Log", command=limpiar_log,
                           bg="#FF5722", fg="white", font=("Arial", 8))
btn_limpiar_log.pack(side=tk.RIGHT)

# Widget de texto con scroll para el log
log_text = scrolledtext.ScrolledText(frame_log, height=8, font=("Consolas", 9),
                                   state=tk.DISABLED, wrap=tk.WORD)
log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

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
agregar_log("🎬 Descargador de YouTube v1.1 - by HanserlodXP", "INFO")
agregar_log("📝 Ingresa una URL de YouTube y presiona 'Obtener Info' para comenzar", "INFO")

# Log de configuración cargada
if config_app.get("ultima_carpeta"):   # type: ignore
    agregar_log(f"📁 Carpeta por defecto: {config_app['ultima_carpeta']}", "INFO")

# Iniciar el bucle principal de la interfaz gráfica
# Esta línea mantiene la ventana abierta y responsiva a los eventos del usuario
ventana.mainloop()