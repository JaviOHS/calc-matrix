from utils.core.resources import resource_path
from PySide6.QtWidgets import QApplication
from utils.core.shortcuts import ShortcutManager
from utils.core.style_manager import StyleManager
from utils.core.font_manager import FontFamily, FontVariant
import sys

def setup_fonts():
    """Configurar las fuentes de la aplicación."""
    main_font = FontFamily("Fira Sans", [
        FontVariant("300", "FiraSans-Light.ttf", "light"),
        FontVariant("400", "FiraSans-Regular.ttf", "regular"),
        FontVariant("500", "FiraSans-Medium.ttf", "medium"),
        FontVariant("600", "FiraSans-SemiBold.ttf", "semibold"),
        FontVariant("700", "FiraSans-Bold.ttf", "bold"),
        FontVariant("800", "FiraSans-ExtraBold.ttf", "extrabold"),
    ])
    
    math_font = FontFamily("Cambria Math", [
        FontVariant("400", "Cambria-Math.ttf", "math")
    ])
    
    return (
        main_font.load(resource_path) and 
        math_font.load(resource_path)
    )

def main():
    """Función principal que inicia la aplicación."""
    app = QApplication(sys.argv)
    
    # Configuración inicial
    if not setup_fonts():
        print("Warning: Some fonts failed to load")
    
    style_manager = StyleManager(resource_path)
    style_variables = style_manager.get_font_variables()
    styles = style_manager.load_styles(style_variables)
    app.setStyleSheet(styles)
    
    # Crear la ventana principal
    from ui.main_window import MainWindow
    window = MainWindow()
    
    # Configurar los atajos de teclado
    shortcuts = ShortcutManager(window, app)
    
    # Iniciar el bucle de eventos
    return sys.exit(app.exec())

if __name__ == "__main__":
    main()
