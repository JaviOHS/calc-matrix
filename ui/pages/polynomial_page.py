from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class PolynomialPage(QWidget):
    def __init__(self):
        super(PolynomialPage, self).__init__()
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        label = QLabel("Operaciones con Polinomios")
        label.setProperty("class", "pages-title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        