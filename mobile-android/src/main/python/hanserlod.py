import yt_dlp
import os
import ffmpeg

def obtener_formatos(url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        format_list = []
        for f in formats:
            itag = f.get('format_id')
            res = f.get('height', 'N/A')
            ext = f.get('ext', 'unknown')
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')
            if vcodec != 'none' or acodec != 'none':
                format_list.append((itag, f"{itag} - {res}p - {ext}"))
        return format_list  # Devuelve lista de tuplas (id, descripción)


def descargar_video(url, output_path, format_id, solo_audio=False):
    # Combinar video+audio para formatos de video
    format_string = f"{format_id}+bestaudio/best" if not solo_audio else format_id

    ydl_opts = {
        'format': format_string,
        'outtmpl': output_path,
        'progress_hooks': [progress_hook],
        'merge_output_format': 'mp4',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if solo_audio:
            video_path = output_path.replace("%(ext)s", "mp4")
            audio_path = output_path.replace("%(ext)s", "mp3")
            ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)
            os.remove(video_path)
            print(f"Archivo convertido a MP3: {audio_path}")

    except yt_dlp.DownloadError as e:
        print(f"Error de descarga: {e}")
        print("Intentando descargar el mejor formato disponible...")
        ydl_opts['format'] = 'best'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def progress_hook(d):

    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        percent = (downloaded / total) * 100
        print(f"Descargando: {percent:.2f}% - {downloaded / (1024 * 1024):.2f} MB de {total / (1024 * 1024):.2f} MB")

    elif d['status'] == 'finished':
        print(f"Descarga terminada: {d['filename']}")

    elif d['status'] == 'error':
        print(f"Error durante la descarga: {d.get('error', 'Desconocido')}")
