#!/usr/bin/env python3
# BTube - by KCorporation
# Versão 1.0.0

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ui.app import BTubeApp

if __name__ == "__main__":
    app = BTubeApp()
    app.mainloop()