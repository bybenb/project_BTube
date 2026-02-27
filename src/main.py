#!/usr/bin/env python3
# BTube - by KCrporation
# Versão 1.0.0

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.app import BTubeApp

if __name__ == "__main__":
    app = BTubeApp()
    app.mainloop()