from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase, QFont

import sys

app = QApplication(sys.argv)

font_id = QFontDatabase.addApplicationFont("assets/fonts/Dosis-Regular.ttf")
families = QFontDatabase.applicationFontFamilies(font_id)
if families:
    font_family = families[0]
else:
    font_family = "Arial"
app.setFont(QFont(font_family, 10))

def load_styles():
    with open("styles/styles.qss", "r") as file:
        style = file.read()
    app.setStyleSheet(style)
load_styles()

window = MainWindow()
window.show()

sys.exit(app.exec())
