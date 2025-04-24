from utils.resources import resource_path
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase
import sys

app = QApplication(sys.argv)

# Configurar la fuente principal 
font_path = resource_path("assets/fonts/Dosis-Regular.ttf")
font_id = QFontDatabase.addApplicationFont(font_path)
families = QFontDatabase.applicationFontFamilies(font_id)

if families:
    font_family = families[0]
else:
    font_family = "Arial"

# Configurar Cambria Math para los exponentes
cambria_math_path = resource_path("assets/fonts/Cambria-Math.ttf")
cambria_math_id = QFontDatabase.addApplicationFont(cambria_math_path)
cambria_families = QFontDatabase.applicationFontFamilies(cambria_math_id)
cambria_family = cambria_families[0] if cambria_families else "Cambria Math"

def load_styles():
    style_path = resource_path("styles/styles.qss")
    with open(style_path, "r") as file:
        style = file.read()
    app.setStyleSheet(style)

load_styles()

window = MainWindow()
window.show()

sys.exit(app.exec())
