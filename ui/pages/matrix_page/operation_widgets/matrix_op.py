from ui.pages.matrix_page.operation_widgets.base_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QSpinBox, QScrollArea, QWidget, QTableWidget, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem, QGridLayout, QSizePolicy)

class MatrixSimpleOP(MatrixOperationWidget):
    def __init__(self, manager, controller, allow_multiple_matrices=True):
        super().__init__(manager, controller, allow_multiple_matrices)
        self.setup_ui()
        
    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Configuración de dimensiones
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        # Dimensiones
        self.dim_label = QLabel("Dimensión de la matriz:" if not self.allow_multiple_matrices else "Dimensión de las matrices (n x n):")
        self.dim_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.dim_spinbox = QSpinBox()
        self.dim_spinbox.setAlignment(Qt.AlignCenter)
        self.dim_spinbox.setRange(1, 10)
        self.dim_spinbox.setValue(4)
        self.dim_spinbox.setObjectName("dim_spinbox")

        config_layout.addWidget(self.dim_label)
        config_layout.addWidget(self.dim_spinbox)
        config_layout.addSpacing(20)

        # Solo mostrar selector de cantidad si se permite más de una matriz
        if self.allow_multiple_matrices:
            self.matrix_count_label = QLabel("Cantidad de matrices:")
            self.matrix_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.matrix_count_spinbox = QSpinBox()
            self.matrix_count_spinbox.setAlignment(Qt.AlignCenter)
            self.matrix_count_spinbox.setRange(2, 10)
            self.matrix_count_spinbox.setValue(2)
            self.matrix_count_spinbox.setObjectName("dim_spinbox")
            
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

        # Creación de botones
        buttons_widget = self.create_buttons()
        self.layout.addWidget(buttons_widget)

        self.setLayout(self.layout)

        # Conexiones
        self.dim_spinbox.valueChanged.connect(self.update_matrix_tables)
        if self.allow_multiple_matrices:
            self.matrix_count_spinbox.valueChanged.connect(self.update_matrix_tables)
        
        # Mostrar matrices iniciales solo si no es una operación especial
        if not hasattr(self, 'skip_initial_matrices'):
            self.update_matrix_tables()
            
    def update_matrix_tables(self):
        """Actualiza las tablas mostrando todas las celdas sin scroll individual"""
        for i in reversed(range(self.matrices_grid.count())): # Limpiar el grid existente
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        dimension = self.dim_spinbox.value()
        matrix_count = self.matrix_count_spinbox.value() if self.allow_multiple_matrices else 1

        cell_size = 50  # Tamaño de cada celda
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
            label = QLabel(f"Matriz {chr(65 + i)}") # A, B, C, ...
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

            # Deshabilitar selección
            table.setSelectionMode(QTableWidget.NoSelection)  # No permite selección alguna
            table.setFocusPolicy(Qt.NoFocus)  # Elimina el rectángulo de enfoque
            
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
        actual_tables = 0 # Verificar cuántas tablas hay en el grid

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
                                return False, f"Valor inválido en Matriz {chr(65 + i)}, fila {r+1}, columna {c+1}"
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
    
class MatrixDeterminant(MatrixSimpleOP):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)
        
class MatrixInverse(MatrixSimpleOP):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)
