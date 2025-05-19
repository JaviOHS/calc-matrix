from PySide6.QtGui import QShortcut, QKeySequence
import os

class ShortcutManager:
    """Gestor de atajos de teclado para CalcMatrix"""
    def __init__(self, main_window, app=None):
        self.window = main_window
        self.app = app
        self.shortcuts = {}
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """Configurar todos los atajos de teclado"""
        # Cerrar aplicación
        self.register_shortcut("Ctrl+Q", self.close_app, "close_app", "Cerrar aplicación")
        
        # Alternar barra lateral
        self.register_shortcut("Ctrl+B", self.toggle_sidebar, "toggle_sidebar", "Abrir/cerrar barra lateral")

        # Abrir página de inicio
        self.register_shortcut("Ctrl+H", lambda: self.window.show_page("home"), "show_home", "Ir a la página de inicio")

        # Abrir página de información
        self.register_shortcut("Ctrl+A", lambda: self.window.show_page("about"), "show_about", "Ir a la página de acerca de")
        
    def register_shortcut(self, key_sequence, callback, shortcut_id, description):
        """Registra un nuevo atajo de teclado"""
        shortcut = QShortcut(QKeySequence(key_sequence), self.window)
        shortcut.activated.connect(callback)
        self.shortcuts[shortcut_id] = {
            "shortcut": shortcut,
            "key_sequence": key_sequence,
            "description": description
        }
    
    def close_app(self):
        """Cierra la aplicación y limpia la consola"""
        if self.app:
            self.app.quit()
            os.system('cls' if os.name == 'nt' else 'clear')
    
    def toggle_sidebar(self):
        """Abre o cierra la barra lateral"""
        # Implementación depende de cómo tienes estructurada tu UI
        if hasattr(self.window, "toggle_sidebar"):
            self.window.toggle_sidebar()
        
    def get_shortcuts_info(self):
        """Retorna información sobre todos los atajos registrados"""
        return {id: {"key": info["key_sequence"], "desc": info["description"]} 
                for id, info in self.shortcuts.items()}
    