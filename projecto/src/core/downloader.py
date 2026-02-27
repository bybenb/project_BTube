import yt_dlp
import threading
import time
import os
from pathlib import Path

class DownloadManager:
    def __init__(self):
        self.downloads = {}
        self.download_count = 0
    
    def add_download(self, url, options, download_id):
        """Adiciona um novo download à fila"""
        
        # Iniciar download em thread
        thread = threading.Thread(
            target=self._download_worker,
            args=(url, options, download_id)
        )
        thread.daemon = True
        thread.start()
    
    def _download_worker(self, url, options, download_id):
        """Worker que executa o download"""
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    percent = d.get('_percent_str', '0%').replace('%', '').strip()
                    speed = d.get('_speed_str', '0 KiB/s').strip()
                    eta = d.get('_eta_str', '--:--').strip()
                    
                    print(f"Download {download_id}: {percent}% - {speed} - {eta}")
                except Exception as e:
                    print(f"Erro no progress hook: {e}")
        
        # Configurar opções do yt-dlp
        ydl_opts = {
            'progress_hooks': [progress_hook],
            'outtmpl': str(Path(options['output_path']) / '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        # Configurar formato baseado na qualidade
        if options.get('quality') == 'bestaudio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': options.get('audio_format', 'mp3'),
                    'preferredquality': '192',
                }]
            })
        else:
            ydl_opts['format'] = options.get('quality', 'best')
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if options.get('quality') == 'bestaudio':
                    filename = filename.rsplit('.', 1)[0] + f".{options.get('audio_format', 'mp3')}"
                
                print(f"Download concluído: {filename}")
                
        except Exception as e:
            print(f"Erro no download: {e}")