from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from ui.widgets.math_operation_widget import MathOperationWidget
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QLabel, QTableWidgetItem, QSpinBox, QScrollArea, QSizePolicy, QGridLayout, QHBoxLayout
from PySide6.QtCore import QEvent, Qt
from model.matrix_model import Matrix
from utils.validators import is_valid_number

class MatrixOperationWidget(MathOperationWidget):
    def __init__(self, manager: MatrixManager, controller: MatrixController, allow_multiple_matrices=True):
        super().__init__(manager, controller)
        self.manager = manager
        self.controller = controller
        self.allow_multiple_matrices = allow_multiple_matrices
        self.tables = []
        self.setup_ui() 

    def setup_ui(self):
        super().setup_ui()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Configuración de dimensiones
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(20, 0, 0, 0)

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

        # Área de scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.matrices_grid = QGridLayout()
        self.matrices_grid.setVerticalSpacing(30)
        self.matrices_grid.setHorizontalSpacing(50)

        self.scroll_layout.addLayout(self.matrices_grid)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Crear botones y conectarlos
        buttons_widget = self.create_buttons()
        self.layout.addWidget(buttons_widget)
        self.calculate_button.clicked.connect(self.execute_operation)
        self.cancel_button.clicked.connect(self.cleanup) 

        self.setLayout(self.layout)

        # Conexiones
        self.dim_spinbox.valueChanged.connect(self.update_matrix_tables)
        if self.allow_multiple_matrices:
            self.matrix_count_spinbox.valueChanged.connect(self.update_matrix_tables)

        if not hasattr(self, 'skip_initial_matrices'):
            self.update_matrix_tables()

        self.scroll_area.viewport().installEventFilter(self)

    def create_table(self, rows, cols, label_text, cell_size=50):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Etiqueta de título de la tabla
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold;")

        # Crear la tabla
        table = QTableWidget()
        table.setRowCount(rows)
        table.setColumnCount(cols)
        
        # Configurar políticas de tamaño
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        
        # Ocultar cabeceras
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setShowGrid(True)
        
        # Configurar tamaño de celdas
        table.horizontalHeader().setDefaultSectionSize(cell_size)
        table.verticalHeader().setDefaultSectionSize(cell_size)
        table.horizontalHeader().setMinimumSectionSize(30)
        table.verticalHeader().setMinimumSectionSize(30)
        table.setWordWrap(False)
        
        # Ajustar el tamaño de la tabla al contenido
        table.setFixedSize(
            cols * cell_size + 2,  # +2 para los bordes
            rows * cell_size + 2 + label.sizeHint().height()  # +2 para bordes + altura de la etiqueta
        )

        # Llenar la tabla con valores predeterminados (1 en todas las celdas)
        for r in range(rows):
            for c in range(cols):
                item = QTableWidgetItem("1")  # Asignar valor por defecto
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)

        layout.addWidget(label)
        layout.addWidget(table, 0, Qt.AlignCenter)

        return {"widget": widget, "table": table, "label": label}

    def update_matrix_tables(self):
        # Limpiar matrices previas
        for i in reversed(range(self.matrices_grid.count())):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        dimension = self.dim_spinbox.value()
        matrix_count = self.matrix_count_spinbox.value() if self.allow_multiple_matrices else 1

        # Obtener el tamaño disponible del área de scroll
        available_width = self.scroll_area.viewport().width() - 20  # Margen de seguridad
        available_height = self.scroll_area.viewport().height() - 20
        spacing = self.matrices_grid.horizontalSpacing()

        # Calcular el número máximo de columnas que caben
        min_table_width = dimension * 30  # Ancho mínimo basado en celdas de 30px
        max_columns = max(1, available_width // (min_table_width + spacing))
        max_columns = min(max_columns, matrix_count)  # No más columnas que matrices

        # Calcular el tamaño de celda óptimo
        if max_columns > 0:
            cell_size_width = max(30, (available_width - (spacing * (max_columns - 1))) // (max_columns * dimension))
            
            # También considerar la altura disponible
            estimated_label_height = 20  # Altura estimada de la etiqueta
            rows_needed = (matrix_count + max_columns - 1) // max_columns
            cell_size_height = max(30, (available_height - (spacing * (rows_needed - 1) - estimated_label_height * rows_needed)) // (rows_needed * dimension))
            
            cell_size = min(cell_size_width, cell_size_height, 40)  # Usar el menor de los dos y limitar a 60px máximo
        else:
            cell_size = 40  # Valor por defecto

        self.tables = []  # Limpiar tablas previas

        # Crear las matrices en la cuadrícula
        for i in range(matrix_count):
            row = i // max_columns
            col = i % max_columns

            label_text = f"Matriz {chr(65 + i)}"
            table_data = self.create_table(dimension, dimension, label_text, cell_size)
            table = table_data["table"]
            widget = table_data["widget"]
            
            # Configurar política de tamaño para el widget contenedor
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setMinimumWidth(dimension * 30)  # Ancho mínimo basado en celdas de 30px
            widget.setMinimumHeight(dimension * 30 + table_data["label"].sizeHint().height())

            self.tables.append(table_data)
            self.matrices_grid.addWidget(widget, row, col, Qt.AlignCenter)

        # Ajustar el espaciado y márgenes
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.matrices_grid.setSpacing(15)
        
        # Forzar actualización del layout
        self.scroll_content.updateGeometry()
        self.scroll_area.updateGeometry()

    def collect_matrices(self):
        matrices = []

        for idx, table_data in enumerate(self.tables):
            table = table_data["table"]
            rows = table.rowCount()
            cols = table.columnCount()
            matrix = Matrix(rows, cols)
            for r in range(rows):
                for c in range(cols):
                    value = table.item(r, c).text()
                    if not is_valid_number(value):
                        raise ValueError(f"Valor inválido en tabla {idx+1} en [{r+1}, {c+1}]: '{value}'")
                    val = float(value)
                    matrix.set_value(r, c, val)
            matrices.append(matrix)

        return matrices

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize and source == self.scroll_area.viewport():
            self.update_matrix_tables()
        return super().eventFilter(source, event)

    def execute_operation(self):
        matrices = self.collect_matrices()

        if isinstance(self, (MatrixDeterminantWidget, MatrixInverseWidget)):
            if len(matrices) != 1:
                raise ValueError("Se requiere exactamente una matriz para calcular el determinante o la inversa.")
        elif len(matrices) < 2:
            raise ValueError("Se requieren al menos dos matrices para realizar la operación.")
        self.manager.matrices.clear()
        for matrix in matrices:
            self.manager.add_matrix(matrix)
        self.cleanup()

class MatrixDeterminantWidget(MatrixOperationWidget):
    def __init__(self, manager: MatrixManager, controller: MatrixController):
        super().__init__(manager, controller, allow_multiple_matrices=False)

class MatrixInverseWidget(MatrixOperationWidget):
    def __init__(self, manager: MatrixManager, controller: MatrixController):
        super().__init__(manager, controller, allow_multiple_matrices=False)
