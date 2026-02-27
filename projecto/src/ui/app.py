import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from pathlib import Path

from core.downloader import DownloadManager
from utils.settings import SettingsManager
from ui.components.download_card import DownloadCard
from ui.components.settings_frame import SettingsFrame

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BTubeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("BTube - downloader de Videos")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # Gerenciadores
        self.settings = SettingsManager()
        self.download_manager = DownloadManager()
        self.download_cards = {}
        
        # Variáveis de controle
        self.current_downloads = 0
        self.max_concurrent = self.settings.get("max_concurrent", 3)
        
        # Configurar UI
        self.setup_ui()
        
        # Carregar configurações
        self.load_settings()
        
        # Bind de fechamento
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Configura toda a interface"""
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar esquerda
        self.setup_sidebar()
        
        # Área principal
        self.setup_main_area()
        
        # Barra de status
        self.setup_status_bar()
    
    def setup_sidebar(self):
        """Sidebar com navegação e controles principais"""
        
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=20, padx=20, fill="x")
        
        logo_label = ctk.CTkLabel(
            logo_frame, 
            text="BTube", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        logo_label.pack()
        
        subtitle = ctk.CTkLabel(
            logo_frame,
            text="downloader de vídeos",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle.pack()
        
        # Separador
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray20").pack(fill="x", padx=20, pady=10)
        
        # Botões de navegação
        self.nav_downloads = ctk.CTkButton(
            self.sidebar,
            text="📥 Downloads",
            command=self.show_downloads,
            anchor="w",
            fg_color="transparent",
            hover_color="gray20"
        )
        self.nav_downloads.pack(pady=5, padx=20, fill="x")
        
        self.nav_library = ctk.CTkButton(
            self.sidebar,
            text="📚 Biblioteca",
            command=self.show_library,
            anchor="w",
            fg_color="transparent",
            hover_color="gray20"
        )
        self.nav_library.pack(pady=5, padx=20, fill="x")
        
        self.nav_settings = ctk.CTkButton(
            self.sidebar,
            text="⚙️ Configurações",
            command=self.show_settings,
            anchor="w",
            fg_color="transparent",
            hover_color="gray20"
        )
        self.nav_settings.pack(pady=5, padx=20, fill="x")
        
        # Espaçador
        ctk.CTkFrame(self.sidebar, fg_color="transparent").pack(expand=True, fill="both")
        
        # Status do KCorp
        kcorp_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        kcorp_frame.pack(pady=20, padx=20, fill="x")
        
        kcorp_label = ctk.CTkLabel(
            kcorp_frame,
            text="KCorporation",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        kcorp_label.pack()
        
        version_label = ctk.CTkLabel(
            kcorp_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=9),
            text_color="gray30"
        )
        version_label.pack()
    
    def setup_main_area(self):
        """Área principal com tabs e conteúdo"""
        
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)
        
        # Header com input
        self.setup_input_header()
        
        # Container para conteúdo
        self.content_container = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.content_container.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        
        # Frames para cada seção
        self.downloads_frame = self.create_downloads_frame()
        self.library_frame = self.create_library_frame()
        self.settings_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        
        # Mostrar downloads por padrão
        self.show_downloads()
    
    def setup_input_header(self):
        """Header com campo de URL e botões"""
        
        header = ctk.CTkFrame(self.main_area, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(0, weight=1)
        
        # Título da seção
        self.section_title = ctk.CTkLabel(
            header,
            text="Downloads Ativos",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.section_title.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Área de input
        input_frame = ctk.CTkFrame(header, fg_color="gray20", corner_radius=10)
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.url_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Cole a URL do vídeo aqui... (YouTube, Vimeo, etc)",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        
        # Frame para botões de ação
        buttons_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=(5, 10))
        
        self.paste_btn = ctk.CTkButton(
            buttons_frame,
            text="📋",
            width=40,
            height=40,
            command=self.paste_url
        )
        self.paste_btn.pack(side="left", padx=2)
        
        self.clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️",
            width=40,
            height=40,
            command=self.clear_url,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.clear_btn.pack(side="left", padx=2)
        
        self.download_btn = ctk.CTkButton(
            buttons_frame,
            text="⬇️ Baixar",
            height=40,
            command=self.start_download,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.download_btn.pack(side="left", padx=2)
        
        # Opções de formato (expansível)
        self.show_options = ctk.CTkCheckBox(
            input_frame,
            text="Mostrar opções avançadas",
            command=self.toggle_options
        )
        self.show_options.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))
        
        # Frame de opções avançadas
        self.options_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        self.options_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.options_frame.grid_columnconfigure(1, weight=1)
        
        # Qualidade
        ctk.CTkLabel(self.options_frame, text="Qualidade:").grid(row=0, column=0, padx=5, pady=5)
        self.quality_var = ctk.StringVar(value="Melhor qualidade")
        quality_combo = ctk.CTkComboBox(
            self.options_frame,
            values=["Melhor qualidade", "720p", "480p", "Apenas áudio"],
            variable=self.quality_var,
            width=200
        )
        quality_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Formato de áudio
        ctk.CTkLabel(self.options_frame, text="Formato áudio:").grid(row=1, column=0, padx=5, pady=5)
        self.audio_format_var = ctk.StringVar(value="mp3")
        audio_combo = ctk.CTkComboBox(
            self.options_frame,
            values=["mp3", "m4a", "wav", "flac"],
            variable=self.audio_format_var,
            width=200
        )
        audio_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Pasta de destino
        ctk.CTkLabel(self.options_frame, text="Salvar em:").grid(row=2, column=0, padx=5, pady=5)
        
        folder_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
        folder_frame.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        folder_frame.grid_columnconfigure(0, weight=1)
        
        self.folder_label = ctk.CTkLabel(
            folder_frame,
            text=str(self.settings.get("download_folder", "Downloads/BTube")),
            anchor="w",
            fg_color="gray30",
            corner_radius=5,
            padx=10,
            pady=5
        )
        self.folder_label.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.browse_btn = ctk.CTkButton(
            folder_frame,
            text="📁",
            width=40,
            command=self.browse_folder
        )
        self.browse_btn.grid(row=0, column=1)
        
        # Inicialmente oculto
        self.options_frame.grid_remove()
    
    def setup_status_bar(self):
        """Barra de status inferior"""
        
        self.status_bar = ctk.CTkFrame(self, height=30, fg_color="gray20")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_bar.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="✅ Pronto para baixar",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, padx=10, sticky="w")
        
        self.stats_label = ctk.CTkLabel(
            self.status_bar,
            text="⬇️ 0 downloads ativos",
            font=ctk.CTkFont(size=11)
        )
        self.stats_label.grid(row=0, column=1, padx=10)
    
    def create_downloads_frame(self):
        """Frame para lista de downloads ativos"""
        
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Canvas com scroll para os cards
        self.downloads_canvas = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        self.downloads_canvas.grid(row=0, column=0, sticky="nsew")
        self.downloads_canvas.grid_columnconfigure(0, weight=1)
        
        # Mensagem quando vazio
        self.empty_downloads_label = ctk.CTkLabel(
            self.downloads_canvas,
            text="✨ Nenhum download ativo\nCole uma URL para começar!",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.empty_downloads_label.grid(row=0, column=0, pady=100)
        
        return frame
    
    def create_library_frame(self):
        """Frame para biblioteca de vídeos baixados"""
        
        frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # Barra de ferramentas
        toolbar = ctk.CTkFrame(frame, fg_color="transparent", height=40)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.refresh_btn = ctk.CTkButton(
            toolbar,
            text="🔄 Atualizar",
            command=self.refresh_library,
            width=100
        )
        self.refresh_btn.pack(side="left", padx=5)
        
        self.open_folder_btn = ctk.CTkButton(
            toolbar,
            text="📂 Abrir pasta",
            command=self.open_downloads_folder,
            width=100,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.open_folder_btn.pack(side="left", padx=5)
        
        # Lista de arquivos
        self.library_list = ctk.CTkScrollableFrame(frame, fg_color="gray20", corner_radius=10)
        self.library_list.grid(row=1, column=0, sticky="nsew")
        self.library_list.grid_columnconfigure(0, weight=1)
        
        # Mensagem quando vazio
        self.empty_library_label = ctk.CTkLabel(
            self.library_list,
            text="📁 Nenhum vídeo baixado ainda",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.empty_library_label.grid(row=0, column=0, pady=100)
        
        return frame
    
    def show_downloads(self):
        """Mostra a aba de downloads"""
        self.section_title.configure(text="Downloads Ativos")
        self.hide_all_frames()
        self.downloads_frame.grid(row=0, column=0, sticky="nsew")
    
    def show_library(self):
        """Mostra a aba de biblioteca"""
        self.section_title.configure(text="Biblioteca")
        self.hide_all_frames()
        self.library_frame.grid(row=0, column=0, sticky="nsew")
        self.refresh_library()
    
    def show_settings(self):
        """Mostra a aba de configurações"""
        self.section_title.configure(text="Configurações")
        self.hide_all_frames()
        self.settings_frame.grid(row=0, column=0, sticky="nsew")
    
    def hide_all_frames(self):
        """Esconde todos os frames de conteúdo"""
        self.downloads_frame.grid_remove()
        self.library_frame.grid_remove()
        self.settings_frame.grid_remove()
    
    def toggle_options(self):
        """Mostra/esconde opções avançadas"""
        if self.show_options.get():
            self.options_frame.grid()
        else:
            self.options_frame.grid_remove()
    
    def paste_url(self):
        """Cola URL da área de transferência"""
        try:
            url = self.clipboard_get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, url)
            self.status_label.configure(text="📋 URL colada com sucesso!")
        except:
            self.status_label.configure(text="❌ Não foi possível colar")
    
    def clear_url(self):
        """Limpa o campo de URL"""
        self.url_entry.delete(0, "end")
        self.status_label.configure(text="🧹 Campo limpo")
    
    def browse_folder(self):
        """Abre diálogo para escolher pasta"""
        folder = filedialog.askdirectory(
            title="Escolher pasta de download",
            initialdir=self.settings.get("download_folder", "")
        )
        if folder:
            self.settings.set("download_folder", folder)
            self.folder_label.configure(text=folder)
    
    def start_download(self):
        """Inicia um novo download"""
        url = self.url_entry.get().strip()
        
        if not url:
            self.status_label.configure(text="⚠️ Por favor, insira uma URL")
            return
        
        # Coletar opções
        options = {
            'quality': self.get_quality_format(),
            'output_path': self.settings.get("download_folder", ""),
            'audio_format': self.audio_format_var.get() if "áudio" in self.quality_var.get().lower() else None
        }
        
        # Criar card de download
        download_id = f"dl_{len(self.download_cards)}"
        card = DownloadCard(
            self.downloads_canvas,
            download_id,
            url[:50] + "..." if len(url) > 50 else url,
            self.quality_var.get(),
            options['output_path']
        )
        card.grid(row=len(self.download_cards), column=0, sticky="ew", pady=5)
        self.download_cards[download_id] = card
        
        # Esconder mensagem vazia
        self.empty_downloads_label.grid_remove()
        
        # Iniciar download em thread
        thread = threading.Thread(
            target=self.download_manager.add_download,
            args=(url, options, download_id)
        )
        thread.daemon = True
        thread.start()
        
        # Limpar campo
        self.url_entry.delete(0, "end")
        self.status_label.configure(text="⬇️ Download adicionado à fila!")
        self.current_downloads += 1
        self.update_stats()
    
    def get_quality_format(self):
        """Converte seleção de qualidade para formato yt-dlp"""
        quality_map = {
            "Melhor qualidade": "best",
            "720p": "best[height<=720]",
            "480p": "best[height<=480]",
            "Apenas áudio": "bestaudio"
        }
        return quality_map.get(self.quality_var.get(), "best")
    
    def refresh_library(self):
        """Atualiza a lista da biblioteca"""
        # Limpar lista atual
        for widget in self.library_list.winfo_children():
            if widget != self.empty_library_label:
                widget.destroy()
        
        # Esconder mensagem vazia
        self.empty_library_label.grid_remove()
        
        # Buscar arquivos
        download_folder = self.settings.get("download_folder", "")
        files_found = False
        
        if os.path.exists(download_folder):
            for file in os.listdir(download_folder):
                if file.endswith(('.mp4', '.mkv', '.webm', '.mp3', '.m4a', '.wav', '.flac')):
                    files_found = True
                    self.add_library_item(file, os.path.join(download_folder, file))
        
        if not files_found:
            self.empty_library_label.grid()
    
    def add_library_item(self, filename, filepath):
        """Adiciona um item à biblioteca"""
        
        item_frame = ctk.CTkFrame(self.library_list, fg_color="gray25", corner_radius=8)
        item_frame.grid(row=len(self.library_list.winfo_children()), column=0, sticky="ew", pady=2, padx=5)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Ícone baseado na extensão
        ext = os.path.splitext(filename)[1].lower()
        icon = "🎵" if ext in ['.mp3', '.m4a', '.wav', '.flac'] else "🎬"
        
        ctk.CTkLabel(item_frame, text=icon, font=ctk.CTkFont(size=16)).grid(row=0, column=0, padx=10, pady=10)
        
        # Nome do arquivo
        name_label = ctk.CTkLabel(
            item_frame,
            text=filename,
            anchor="w",
            font=ctk.CTkFont(size=12)
        )
        name_label.grid(row=0, column=1, sticky="w", padx=5)
        
        # Botões
        play_btn = ctk.CTkButton(
            item_frame,
            text="▶️",
            width=40,
            command=lambda: self.play_file(filepath),
            fg_color="transparent",
            hover_color="gray40"
        )
        play_btn.grid(row=0, column=2, padx=2)
        
        folder_btn = ctk.CTkButton(
            item_frame,
            text="📂",
            width=40,
            command=lambda: self.open_file_location(filepath),
            fg_color="transparent",
            hover_color="gray40"
        )
        folder_btn.grid(row=0, column=3, padx=2)
    
    def play_file(self, filepath):
        """Abre o arquivo com o player padrão"""
        import subprocess
        import platform
        import os
        
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', filepath])
        else:
            subprocess.run(['xdg-open', filepath])
    
    def open_file_location(self, filepath):
        """Abre a pasta contendo o arquivo"""
        import subprocess
        import platform
        import os
        
        folder = os.path.dirname(filepath)
        
        if platform.system() == 'Windows':
            os.startfile(folder)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', folder])
        else:
            subprocess.run(['xdg-open', folder])
    
    def open_downloads_folder(self):
        """Abre a pasta de downloads"""
        import platform
        import os
        
        folder = self.settings.get("download_folder", "")
        if os.path.exists(folder):
            if platform.system() == 'Windows':
                os.startfile(folder)
    
    def update_stats(self):
        """Atualiza estatísticas na barra de status"""
        self.stats_label.configure(
            text=f"⬇️ {self.current_downloads} downloads ativos | 📁 {self.get_library_count()} arquivos"
        )
    
    def get_library_count(self):
        """Conta arquivos na biblioteca"""
        folder = self.settings.get("download_folder", "")
        count = 0
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(('.mp4', '.mkv', '.webm', '.mp3', '.m4a', '.wav', '.flac')):
                    count += 1
        return count
    
    def load_settings(self):
        """Carrega configurações salvas"""
        self.folder_label.configure(
            text=self.settings.get("download_folder", "Downloads/BTube")
        )
        self.max_concurrent = self.settings.get("max_concurrent", 3)
    
    def on_closing(self):
        """Quando a janela é fechada"""
        self.settings.save()
        self.destroy()

if __name__ == "__main__":
    app = BTubeApp()
    app.mainloop()