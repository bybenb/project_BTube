import sys
import os

# Adiciona src ao path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

from ui.app import BTubeApp

if __name__ == "__main__":
    app = BTubeApp()
    app.mainloop()



# pyinstaller --name "BTube" ^ --windowed ^ --onefile ^ --add-data "src;src" ^ --hidden-import customtkinter ^ --hidden-import yt_dlp ^ --hidden-import mutagen ^ --hidden-import requests ^ --paths src ^ run.py 
