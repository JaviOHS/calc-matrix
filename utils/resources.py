import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta correcta tanto en dev como en el ejecutable .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
