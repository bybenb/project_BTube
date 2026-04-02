import json
import os
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.config_dir = Path.home() / '.btube'
        self.config_file = self.config_dir / 'settings.json'
        
        self.default_settings = {
            'download_folder': str(Path.home() / 'Downloads' / 'BTube'),
            'max_concurrent': 3,
            'default_quality': 'best',
            'theme': 'dark',
            'notifications': True,
            'auto_open_folder': False
        }
        
        self.settings = self.load()
        self.ensure_download_folder()
    
    def load(self):
        """Carrega configurações do arquivo"""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return {**self.default_settings, **loaded}
            except:
                return self.default_settings.copy()
        
        return self.default_settings.copy()
    
    def save(self):
        """Salva configurações no arquivo"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    def get(self, key, default=None):
        """Retorna uma configuração"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Define uma configuração"""
        self.settings[key] = value
        self.save()
    
    def ensure_download_folder(self):
        """Garante que a pasta de download existe"""
        folder = Path(self.settings['download_folder'])
        if not folder.exists():
            folder.mkdir(parents=True)