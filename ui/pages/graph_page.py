from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class GraphPage(QWidget):
    def __init__(self, parent=None):
        super(GraphPage, self).__init__(parent)
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()
        label = QLabel("Operaciones con Gráficos")
        label.setProperty("class", "pages-title")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)