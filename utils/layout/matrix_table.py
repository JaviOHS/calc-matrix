from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QLabel, QTableWidgetItem, QHeaderView, QSizePolicy
from PySide6.QtCore import Qt
import random

class MatrixTableComponent:
    @staticmethod
    def create_table(rows, cols, label_text="", cell_size=50, random_fill=True):
        """Crea un componente de tabla de matriz con etiqueta"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Etiqueta de título
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)

        # Crear tabla
        table = QTableWidget()
        table.setRowCount(rows)
        table.setColumnCount(cols)
        
        # Configurar tabla
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setShowGrid(True)
        
        # Configurar tamaño de celdas
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setMinimumSectionSize(30)
        table.verticalHeader().setMinimumSectionSize(30)
        table.setWordWrap(False)
        table.setMaximumSize(cols * cell_size + 4, rows * cell_size + 4)

        # Llenar con valores aleatorios si se solicita
        if random_fill:
            MatrixTableComponent.fill_random_values(table, rows, cols)

        layout.addWidget(label)
        layout.addWidget(table, 0, Qt.AlignCenter)

        return {"widget": widget, "table": table, "label": label}
    
    @staticmethod
    def fill_random_values(table, rows, cols, min_val=1, max_val=9):
        """Rellena la tabla con valores aleatorios"""
        for r in range(rows):
            for c in range(cols):
                random_value = random.randint(min_val, max_val)
                item = QTableWidgetItem(str(random_value))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)
                