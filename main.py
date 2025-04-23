from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase, QFont
import os 
import sys

def resource_path(relative_path):
    """Obtiene la ruta correcta tanto en dev como en el ejecutable .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = QApplication(sys.argv)

# Configurar la fuente principal 
font_id = QFontDatabase.addApplicationFont("assets/fonts/Dosis-Regular.ttf")
families = QFontDatabase.applicationFontFamilies(font_id)
if families:
    font_family = families[0]
else:
    font_family = "Arial"

# Configurar Cambria Math para los exponentes
cambria_math_id = QFontDatabase.addApplicationFont("assets/fonts/Cambria-Math.ttf")
cambria_families = QFontDatabase.applicationFontFamilies(cambria_math_id)
cambria_family = cambria_families[0] if cambria_families else "Cambria Math"

app.setFont(QFont(font_family, 10))

def load_styles():
    with open("styles/styles.qss", "r") as file:
        style = file.read()
    app.setStyleSheet(style)
load_styles()

window = MainWindow()
window.show()

sys.exit(app.exec())
