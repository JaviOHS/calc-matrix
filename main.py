from utils.resources import resource_path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase
from utils.shortcuts import ShortcutManager
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

def load_styles(app, font_family):
    """Cargar hojas de estilo modulares."""
    style_files = [
        "base.qss",
        "layout.qss", 
        "pages.qss",
        "components.qss",
        "buttons.qss",
        "inputs.qss",
        "scrollbars.qss",
        "dialogs.qss"
    ]
    
    combined_styles = ""
    
    # Combinar todos los archivos en el orden especificado
    for style_file in style_files:
        file_path = resource_path(f"styles/{style_file}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                combined_styles += file.read() + "\n\n"
        except FileNotFoundError:
            print(f"Advertencia: Archivo de estilo no encontrado: {style_file}")
    
    combined_styles = combined_styles.replace("{{FONT_FAMILY}}", font_family)
    app.setStyleSheet(combined_styles)

def main():
    """Función principal que inicia la aplicación."""
    app = QApplication(sys.argv)
    
    # Configuración inicial
    font_family, cambria_family = setup_fonts()
    load_styles(app, font_family)
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    
    # Configurar los atajos de teclado
    shortcuts = ShortcutManager(window, app)
    
    window.show()
    
    # Iniciar el bucle de eventos
    return sys.exit(app.exec())

if __name__ == "__main__":
    main()
