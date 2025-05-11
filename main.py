from utils.resources import resource_path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase, QShortcut, QKeySequence
import os
import sys

def setup_fonts():
    """Configurar las fuentes de la aplicación."""
    font_path = resource_path("assets/fonts/FiraSans-Regular.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    families = QFontDatabase.applicationFontFamilies(font_id)
    font_family = families[0] if families else "Arial"
    
    cambria_math_path = resource_path("assets/fonts/Cambria-Math.ttf")
    cambria_math_id = QFontDatabase.addApplicationFont(cambria_math_path)
    cambria_families = QFontDatabase.applicationFontFamilies(cambria_math_id)
    cambria_family = cambria_families[0] if cambria_families else "Cambria Math"
    
    return font_family, cambria_family

def load_styles(app):
    """Cargar hojas de estilo."""
    style_path = resource_path("styles/styles.qss")
    with open(style_path, "r") as file:
        style = file.read()
    app.setStyleSheet(style)

def setup_shortcuts(window, app):
    """Configurar atajos de teclado."""
    # Crear atajo para cerrar y limpiar consola (Ctrl+Q)
    def close_and_clear():
        app.quit()
        os.system('cls' if os.name == 'nt' else 'clear')

    shortcut = QShortcut(QKeySequence("Ctrl+Q"), window)
    shortcut.activated.connect(close_and_clear)

def main():
    """Función principal que inicia la aplicación."""
    app = QApplication(sys.argv)
    
    # Configuración inicial
    font_family, cambria_family = setup_fonts()
    load_styles(app)
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    setup_shortcuts(window, app)
    window.show()
    
    # Iniciar el bucle de eventos
    return sys.exit(app.exec())

if __name__ == "__main__":
    main()
    