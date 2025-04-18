from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super(AboutPage, self).__init__(parent)
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        label = QLabel("Acerca de la Aplicación")
        label.setProperty("class", "pages-title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)