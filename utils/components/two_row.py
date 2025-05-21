from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QGroupBox

class TwoRowWidget(QWidget):
    """Componente que organiza el contenido en dos filas: una para inputs/labels y otra para matrices"""
    
    def __init__(self, row1_label=None, row2_label=None, parent=None):
        super().__init__(parent)
        self.row1_label = row1_label
        self.row2_label = row2_label

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 20, 0)
        self.layout.setSpacing(10)

        # Primera fila (inputs y labels)
        self.row1_group = QGroupBox(f"📌 {self.row1_label}" if self.row1_label else "Configuración")
        self.row1_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.row1_layout = QGridLayout(self.row1_group)
        self.row1_layout.setContentsMargins(5, 5, 5, 5)
        self.row1_layout.setSpacing(5)

        # Segunda fila (matrices)
        self.row2_group = QGroupBox(f"📌 {self.row2_label}" if self.row2_label else "Matrices")
        self.row2_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.row2_layout = QGridLayout(self.row2_group)
        self.row2_layout.setContentsMargins(5, 0, 5, 0)
        self.row2_layout.setSpacing(10)

        # Añadir filas al layout principal
        self.layout.addWidget(self.row1_group)
        self.layout.addWidget(self.row2_group)

    def add_to_row1(self, widget, row=0, col=0, rowspan=1, colspan=1):
        """Añade un widget a la primera fila en la posición especificada"""
        self.row1_layout.addWidget(widget, row, col, rowspan, colspan)

    def add_to_row2(self, widget, row=0, col=0, rowspan=1, colspan=1):
        """Añade un widget a la segunda fila en la posición especificada"""
        self.row2_layout.addWidget(widget, row, col, rowspan, colspan)

    def clear_row1(self):
        """Limpia todos los widgets en la primera fila"""
        while self.row1_layout.count():
            item = self.row1_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def clear_row2(self):
        """Limpia todos los widgets en la segunda fila"""
        while self.row2_layout.count():
            item = self.row2_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()