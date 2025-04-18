from ui.pages.matrix_page.operation_widgets.base_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QSpinBox, QScrollArea, QWidget, QTableWidget, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem, QGridLayout, QSizePolicy)

class MatrixAddSubWidget(MatrixOperationWidget):
    def __init__(self, manager, controller, allow_multiple_matrices=True):
        super().__init__(manager, controller, allow_multiple_matrices)
        
    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        # Configuración de dimensiones
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        # Dimensiones
        dim_label = QLabel("Dimensión de las matrices (n x n):")
        dim_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.dim_spinbox = QSpinBox()
        self.dim_spinbox.setAlignment(Qt.AlignCenter)
        self.dim_spinbox.setRange(1, 10)
        self.dim_spinbox.setValue(4)
        self.dim_spinbox.setObjectName("dim_spinbox")  
        
        # Cantidad de matrices
        self.matrix_count_label = QLabel("Cantidad de matrices:")
        self.matrix_count_label.setAlignment(Qt.AlignCenter)
        self.matrix_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.matrix_count_spinbox = QSpinBox()
        self.matrix_count_spinbox.setAlignment(Qt.AlignCenter)
        self.matrix_count_spinbox.setObjectName("dim_spinbox")
        
        config_layout.addWidget(dim_label)
        config_layout.addWidget(self.dim_spinbox)
        config_layout.addSpacing(20)
        config_layout.addWidget(self.matrix_count_label)
        config_layout.addWidget(self.matrix_count_spinbox)
        config_layout.addStretch()

        self.layout.addWidget(config_widget)

        # Área de scroll principal
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Contenedor principal para las matrices
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        
        # Grid para organizar las matrices (2 por fila)
        self.matrices_grid = QGridLayout()
        self.matrices_grid.setVerticalSpacing(30)
        self.matrices_grid.setHorizontalSpacing(50)
        
        self.scroll_layout.addLayout(self.matrices_grid)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Botones
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        
        self.cancel_button = QPushButton("Cancelar")
        self.calculate_button = QPushButton("Calcular")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.calculate_button)
        
        self.layout.addWidget(buttons_widget)

        self.setLayout(self.layout)

        # Conexiones
        self.dim_spinbox.valueChanged.connect(self.update_matrix_tables)
        self.matrix_count_spinbox.valueChanged.connect(self.update_matrix_tables)

        self.configure_matrix_count_spinbox()
        self.update_matrix_tables()

    def configure_matrix_count_spinbox(self):
        if self.allow_multiple_matrices:
            self.matrix_count_spinbox.setRange(2, 10)
            self.matrix_count_spinbox.setValue(2)
            self.matrix_count_spinbox.setEnabled(True)
            self.matrix_count_label.show()
            self.matrix_count_spinbox.show()
        else:
            self.matrix_count_spinbox.setRange(1, 1)
            self.matrix_count_spinbox.setValue(1)
            self.matrix_count_spinbox.setEnabled(False)
            self.matrix_count_label.hide()
            self.matrix_count_spinbox.hide()

    def update_matrix_tables(self):
        """Actualiza las tablas mostrando todas las celdas sin scroll individual"""
        # Limpiar el grid existente
        for i in reversed(range(self.matrices_grid.count())): 
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        dimension = self.dim_spinbox.value()
        matrix_count = self.matrix_count_spinbox.value()
        
        # Calcular tamaño necesario para las tablas
        cell_size = 40  # Tamaño de cada celda
        table_size = dimension * cell_size + 2  # +2 por los bordes
        
        # Crear matrices en grid de 2 columnas
        for i in range(matrix_count):
            row = i // 2
            col = i % 2
            
            # Widget contenedor para cada matriz
            matrix_widget = QWidget()
            matrix_layout = QVBoxLayout(matrix_widget)
            matrix_layout.setContentsMargins(0, 0, 0, 0)
            matrix_layout.setSpacing(5)
            
            # Etiqueta de la matriz
            label = QLabel(f"Matriz {i+1}")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold;")
            
            # Tabla de la matriz
            table = QTableWidget()
            table.setRowCount(dimension)
            table.setColumnCount(dimension)
            
            # Configurar tabla para mostrar todo sin scroll
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            
            # Tamaño fijo para mostrar todas las celdas
            table.setFixedSize(table_size, table_size)
            
            # Configurar encabezados y celdas
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setDefaultSectionSize(cell_size)
            table.verticalHeader().setDefaultSectionSize(cell_size)
            table.setShowGrid(True)
            
            # Inicializar celdas
            for r in range(dimension):
                for c in range(dimension):
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignCenter)
                    table.setItem(r, c, item)
            
            matrix_layout.addWidget(label)
            matrix_layout.addWidget(table, 0, Qt.AlignCenter)
            
            self.matrices_grid.addWidget(matrix_widget, row, col, Qt.AlignCenter)

    def validate_operation(self):
        dimension = self.dim_spinbox.value()
        matrix_count = self.matrix_count_spinbox.value()
        
        # Verificar que tenemos todas las tablas
        actual_tables = 0
        for i in range(self.matrices_grid.count()):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget and widget.findChild(QTableWidget):
                actual_tables += 1
        
        if actual_tables != matrix_count:
            return False, "Número incorrecto de matrices"
        
        # Verificar valores en las tablas
        for i in range(self.matrices_grid.count()):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                table = widget.findChild(QTableWidget)
                if table:
                    for r in range(dimension):
                        for c in range(dimension):
                            item = table.item(r, c)
                            if not item or not item.text().replace('.', '').replace('-', '').isdigit():
                                return False, f"Valor inválido en Matriz {i+1}, fila {r+1}, columna {c+1}"
        
        return True, ""
    
    def collect_matrices(self):
        dimension = self.dim_spinbox.value()
        matrices = []
        
        for i in range(self.matrices_grid.count()):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                table = widget.findChild(QTableWidget)
                if table:
                    matrix = Matrix(dimension, dimension)
                    for r in range(dimension):
                        for c in range(dimension):
                            value = float(table.item(r, c).text())
                            matrix.set_value(r, c, value)
                    matrices.append(matrix)
        
        return matrices