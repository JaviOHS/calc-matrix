from ui.widgets.math_operation_widget import MathOperationWidget
from utils.components.ui_utils import UIUtils
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtCore import QEvent, Qt
from model.matrix_model import Matrix
from utils.validators.matrix_validator import MatrixValidator
from utils.components.two_row import TwoRowWidget
from utils.components.dimension_config_utils import DimensionConfigUtils
from utils.components.matrix_grid_utils import MatrixGridUtils

class MatrixBaseOp(MathOperationWidget):
    def __init__(self, manager, controller, allow_multiple_matrices=True):
        super().__init__(manager, controller)
        self.manager = manager
        self.controller = controller
        self.allow_multiple_matrices = allow_multiple_matrices
        self.tables = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.two_row_widget = TwoRowWidget(row1_label="Configuración de Matrices", row2_label="Área de Matrices")
        self.two_row_widget.setContentsMargins(20, 0, 20, 0)
        
        main_layout.addWidget(self.two_row_widget)

        self._setup_dimension_config()
        self._setup_matrices_area()

        # Crear botones de acción
        buttons_widget = self.create_buttons()
        buttons_widget.setContentsMargins(20, 10, 20, 10)
        main_layout.addWidget(buttons_widget)

        # Conectar señales
        self._connect_signals()
        
        # Inicializar matrices si es necesario
        if not hasattr(self, 'skip_initial_matrices'):
            self.update_matrix_tables()

    def _setup_dimension_config(self):
        """Configura los widgets de dimensión en la primera fila"""
        config_widget, self.dim_spinbox, self.matrix_count_spinbox = DimensionConfigUtils.create_dimension_config(self.allow_multiple_matrices)
        self.two_row_widget.add_to_row1(config_widget)

    def _setup_matrices_area(self):
        """Configura el área de matrices en la segunda fila"""
        self.scroll_area, self.matrices_grid = UIUtils.create_matrix_grid_area(self.dim_spinbox.value(), self.matrix_count_spinbox.value() if self.allow_multiple_matrices else 1)
        self.two_row_widget.add_to_row2(self.scroll_area)

    def _connect_signals(self):
        """Conecta señales de los controles"""
        self.dim_spinbox.valueChanged.connect(self.update_matrix_tables)
        if self.allow_multiple_matrices and hasattr(self, 'matrix_count_spinbox'):
            self.matrix_count_spinbox.valueChanged.connect(self.update_matrix_tables)
        self.scroll_area.viewport().installEventFilter(self)

    def update_matrix_tables(self):
        # Limpiar matrices previas
        for i in reversed(range(self.matrices_grid.count())):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        dimension = self.dim_spinbox.value()
        matrix_count = self.matrix_count_spinbox.value() if self.allow_multiple_matrices else 1

        # Calcular layout óptimo
        max_columns, cell_size = MatrixGridUtils.calculate_matrix_layout(self.scroll_area,  dimension,  matrix_count)
        self.tables = []
        
        # Crear las matrices en la cuadrícula
        for i in range(matrix_count):
            row = i // max_columns
            col = i % max_columns
            
            table_data = MatrixGridUtils.create_matrix_widget(dimension, i, cell_size)
            self.tables.append(table_data)
            self.matrices_grid.addWidget(table_data["widget"], row, col, Qt.AlignCenter)
            
        self.matrices_grid.setSpacing(15)

    def collect_matrices(self):
        matrices = []

        for idx, table_data in enumerate(self.tables):
            table = table_data["table"]
            rows = table.rowCount()
            cols = table.columnCount()
            
            # Validar valores usando el validador centralizado
            matrix_name = f"Matriz {chr(65 + idx)}"
            values = MatrixValidator.validate_table_values(table, matrix_name)
            
            # Crear la matriz con los valores validados
            matrix = Matrix(rows, cols)
            for r in range(rows):
                for c in range(cols):
                    matrix.set_value(r, c, values[r][c])
                    
            matrices.append(matrix)

        return matrices

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize and source == self.scroll_area.viewport():
            self.update_matrix_tables()
        return super().eventFilter(source, event)

    def execute_operation(self):
        """Método base para ejecutar operaciones matriciales"""
        try:
            matrices = self.collect_matrices() # Recolectar matrices
            self.manager.matrices.clear()
            for matrix in matrices:
                self.manager.add_matrix(matrix)
                
            operation_key = self._get_operation_key()            
            result = self.controller.execute_operation(operation_key)
            return result
            
        except ValueError as e:
            raise ValueError(str(e))
    
    def _get_operation_key(self):
        """Obtiene la clave de operación asociada a este widget."""
        for label, (key, widget_class) in getattr(self.parent(), 'operations', {}).items():
            if isinstance(self, widget_class):
                return key
        raise ValueError("No se pudo determinar la operación para este widget.")

class OneMatrixOpWidget(MatrixBaseOp):
    """Clase base para operaciones con una sola matriz (ej. Transpuesta, Determinante)"""
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)
        self.skip_initial_matrices = True