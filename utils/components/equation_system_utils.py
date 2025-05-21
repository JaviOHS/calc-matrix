from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHeaderView
from PySide6.QtCore import Qt
from utils.layout.matrix_table import MatrixTableComponent

class EquationSystemUtils:
    @staticmethod
    def create_equation_system_widget(dimension, cell_size=50):
        """Crea un widget para el sistema de ecuaciones"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        container_layout.setAlignment(Qt.AlignTop)

        # Crear tabla
        table_data = MatrixTableComponent.create_table(dimension,  dimension + 1, "", cell_size=cell_size, random_fill=True)
        system_table = table_data["table"]
        
        # Configurar cabeceras
        headers = [f"x{i+1}" for i in range(dimension)] + ["= b"]
        system_table.setHorizontalHeaderLabels(headers)
        system_table.horizontalHeader().setVisible(True)
        
        # Configurar header
        header = system_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        
        # Ajustar tamaño
        system_table.setFixedSize((dimension + 1) * cell_size + 2, (dimension * cell_size) + header.sizeHint().height() + 2)
        container_layout.addWidget(table_data["widget"], 0, Qt.AlignHCenter | Qt.AlignTop)
        
        return {
            "container": container,
            "table": system_table,
            "widget": table_data["widget"]
        }