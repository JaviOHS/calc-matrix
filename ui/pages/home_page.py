from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super(HomePage, self).__init__()
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        # ---------- Título de páginas ----------
        title_label = QLabel("Bienvenido a la Calculadora")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)
        self.setLayout(layout)

        # ---------- Texto de introducción ----------
        label = QLabel("Este proyecto consiste en una calculadora para realizar operaciones matemáticas y algebraicas.\n""Puedes usar los botones de la barra lateral para navegar por las diferentes secciones o escoger los botones que se encuentran aquí abajo. 😉")
        label.setAlignment(Qt.AlignLeft)
        label.setWordWrap(True)
        label.setOpenExternalLinks(True)
        layout.addWidget(label)