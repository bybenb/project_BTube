"""
    Ben McBridge 
    Christhopher McBridge

    McBridge Brothers
"""


import customtkinter as ctk
import time

class DownloadCard(ctk.CTkFrame):
    def __init__(self, parent, download_id, title, quality, output_path):
        super().__init__(parent, fg_color="gray25", corner_radius=10)
        
        self.download_id = download_id
        self.title = title
        self.status = "pending"
        
        self.setup_ui(title, quality, output_path)
        
    def setup_ui(self, title, quality, output_path):
        self.grid_columnconfigure(1, weight=1)
        
        self.status_icon = ctk.CTkLabel(
            self,
            text="⏳",
            font=ctk.CTkFont(size=20)
        )
        self.status_icon.grid(row=0, column=0, padx=(15, 5), pady=15)
        
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        info_frame.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(
            info_frame,
            text=title[:50] + "..." if len(title) > 50 else title,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        

        details_text = f" {quality} | 📁 {output_path[:30]}..."
        self.details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        self.details_label.grid(row=1, column=0, sticky="w", pady=(2, 5))
        
        self.progress_bar = ctk.CTkProgressBar(info_frame)
        self.progress_bar.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        self.progress_bar.set(0)
        
        speed_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        speed_frame.grid(row=3, column=0, sticky="ew", pady=(2, 0))
        
        self.speed_label = ctk.CTkLabel(
            speed_frame,
            text="baixando 0 KB/s",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.speed_label.pack(side="left")
        
        self.eta_label = ctk.CTkLabel(
            speed_frame,
            text="⏱️ --:--",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.eta_label.pack(side="right")
        
        
        
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=2, padx=(5, 15))
        
        self.pause_btn = ctk.CTkButton(
            btn_frame,
            text="⏸️",
            width=30,
            height=30,
            command=self.pause_download,
            fg_color="transparent",
            hover_color="gray40"
        )
        self.pause_btn.pack(side="top", pady=2)
        
        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌",
            width=30,
            height=30,
            command=self.cancel_download,
            fg_color="transparent",
            hover_color="red"
        )
        self.cancel_btn.pack(side="top", pady=2)
    
    def update_progress(self, progress_data):
        """Atualiza o progresso do download"""
        percent = progress_data.get('percent', 0) / 100
        self.progress_bar.set(percent)
        
        self.speed_label.configure(
            text=f"🚀 {progress_data.get('speed', '0 KB/s')}"
        )
        
        eta = progress_data.get('eta', '--:--')
        if eta != 'N/A':
            self.eta_label.configure(text=f"⏱️ {eta}")
        
        if self.status == "pending":
            self.status_icon.configure(text="⬇️")
            self.status = "downloading"
    
    def complete(self):
        """Marca como concluído"""
        self.status_icon.configure(text="✅")
        self.progress_bar.set(1)
        self.speed_label.configure(text=" Concluído!")
        self.eta_label.configure(text="")
        
        
        self.pause_btn.configure(state="disabled")
        self.cancel_btn.configure(text="🗑️", command=self.remove)
    
    def show_error(self, error_msg):
        """Mostra erro no download"""
        self.status_icon.configure(text="❌")
        self.details_label.configure(
            text=f"Erro: {error_msg[:50]}...",
            text_color="red"
        )
    
    def pause_download(self):
        """Pausa o download"""
        self.status_icon.configure(text="⏸️")
    
    def cancel_download(self):
        """Cancela o download"""
        self.status_icon.configure(text="🗑️")
    
    def remove(self):
        """Remove o card"""
        self.destroy()