import customtkinter as ctk
from tkinter import filedialog
import os

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, settings_manager):
        super().__init__(parent, fg_color="transparent")
        
        self.settings = settings_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface de configurações"""
        
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            self,
            text="⚙️ Configurações",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, pady=(0, 30), sticky="w")
        
        settings_container = ctk.CTkFrame(self, fg_color="gray20", corner_radius=10)
        settings_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        settings_container.grid_columnconfigure(1, weight=1)
        
        current_row = 0
        
        ctk.CTkLabel(
            settings_container,
            text="📁 Pasta de Download:",
            font=ctk.CTkFont(size=14)
        ).grid(row=current_row, column=0, padx=20, pady=15, sticky="w")
        
        folder_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        folder_frame.grid(row=current_row, column=1, padx=20, pady=15, sticky="ew")
        folder_frame.grid_columnconfigure(0, weight=1)
        
        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            textvariable=ctk.StringVar(value=self.settings.get("download_folder", "")),
            height=35
        )
        self.folder_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_btn = ctk.CTkButton(
            folder_frame,
            text="📂",
            width=40,
            height=35,
            command=self.browse_folder
        )
        self.browse_btn.grid(row=0, column=1)
        
        current_row += 1
        
        ctk.CTkFrame(settings_container, height=2, fg_color="gray40").grid(
            row=current_row, column=0, columnspan=2, sticky="ew", padx=20, pady=10
        )
        current_row += 1
        

        ctk.CTkLabel(
            settings_container,
            text="⬇️ Downloads Simultâneos:",
            font=ctk.CTkFont(size=14)
        ).grid(row=current_row, column=0, padx=20, pady=15, sticky="w")
        
        self.concurrent_var = ctk.IntVar(value=self.settings.get("max_concurrent", 3))
        concurrent_slider = ctk.CTkSlider(
            settings_container,
            from_=1,
            to=5,
            number_of_steps=4,
            variable=self.concurrent_var,
            command=self.on_concurrent_change,
            width=300
        )
        concurrent_slider.grid(row=current_row, column=1, padx=20, pady=15, sticky="w")
        
        self.concurrent_label = ctk.CTkLabel(
            settings_container,
            text=f"{self.concurrent_var.get()} downloads",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.concurrent_label.grid(row=current_row, column=1, padx=(350, 0), pady=15, sticky="w")
        
        current_row += 1
        
        ctk.CTkFrame(settings_container, height=2, fg_color="gray40").grid(
            row=current_row, column=0, columnspan=2, sticky="ew", padx=20, pady=10
        )
        current_row += 1
        
        ctk.CTkLabel(
            settings_container,
            text="Qualidade Padrão:",
            font=ctk.CTkFont(size=14)
        ).grid(row=current_row, column=0, padx=20, pady=15, sticky="w")
        
        self.quality_var = ctk.StringVar(value=self.settings.get("default_quality", "Melhor qualidade"))
        quality_combo = ctk.CTkComboBox(
            settings_container,
            values=["Melhor qualidade", "720p", "480p", "Apenas áudio"],
            variable=self.quality_var,
            width=200,
            command=self.on_quality_change
        )
        quality_combo.grid(row=current_row, column=1, padx=20, pady=15, sticky="w")
        
        current_row += 1
        
        ctk.CTkLabel(
            settings_container,
            text="🔔 Notificações:",
            font=ctk.CTkFont(size=14)
        ).grid(row=current_row, column=0, padx=20, pady=15, sticky="w")
        
        self.notifications_var = ctk.BooleanVar(value=self.settings.get("notifications", True))
        notifications_switch = ctk.CTkSwitch(
            settings_container,
            text="Ativar notificações",
            variable=self.notifications_var,
            command=self.on_notifications_change
        )
        notifications_switch.grid(row=current_row, column=1, padx=20, pady=15, sticky="w")
        
        current_row += 1
        
        ctk.CTkFrame(settings_container, height=2, fg_color="gray40").grid(
            row=current_row, column=0, columnspan=2, sticky="ew", padx=20, pady=10
        )
        current_row += 1
        
        buttons_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        buttons_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
        
        self.save_btn = ctk.CTkButton(
            buttons_frame,
            text="Salvar Configurações",
            command=self.save_settings,
            height=40,
            width=200,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.save_btn.pack(side="left", padx=10)
        
        self.reset_btn = ctk.CTkButton(
            buttons_frame,
            text="Restaurar Padrões",
            command=self.reset_settings,
            height=40,
            width=200,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.reset_btn.pack(side="left", padx=10)
    
    def browse_folder(self):
        """Abre diálogo para escolher pasta"""
        folder = filedialog.askdirectory(
            title="Escolher pasta de download",
            initialdir=self.settings.get("download_folder", "")
        )
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
    
    def on_concurrent_change(self, value):
        """Atualiza label quando o slider muda"""
        self.concurrent_label.configure(text=f"{int(value)} downloads")
    
    def on_quality_change(self, choice):
        """Quando a qualidade padrão muda"""
        pass
    
    def on_notifications_change(self):
        """Quando o switch de notificações muda"""
        pass
    
    def save_settings(self):
        """Salva as configurações"""
        self.settings.set("download_folder", self.folder_entry.get())
        self.settings.set("max_concurrent", int(self.concurrent_var.get()))
        self.settings.set("default_quality", self.quality_var.get())
        self.settings.set("notifications", self.notifications_var.get())
        
        self.save_btn.configure(text=" Salvo!", fg_color="green")
        self.after(2000, lambda: self.save_btn.configure(text="Salvar Configurações", fg_color="#1f538d"))
    
    def reset_settings(self):
        """Restaura configurações padrão"""
        self.settings.reset()
        
        
        
        
        self.folder_entry.delete(0, "end")
        self.folder_entry.insert(0, self.settings.get("download_folder", ""))
        
        self.concurrent_var.set(self.settings.get("max_concurrent", 3))
        self.concurrent_label.configure(text=f"{self.concurrent_var.get()} downloads")
        
        self.quality_var.set(self.settings.get("default_quality", "Melhor qualidade"))
        self.notifications_var.set(self.settings.get("notifications", True))