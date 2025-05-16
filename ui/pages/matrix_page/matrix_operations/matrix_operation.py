from ui.widgets.math_operation_widget import MathOperationWidget
from utils.matrix_table import MatrixTableComponent
from utils.ui_utils import UIUtils
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QEvent, Qt
from model.matrix_model import Matrix
from utils.validators.matrix_validator import MatrixValidator
from utils.spinbox_utils import create_int_spinbox

class MatrixOperationWidget(MathOperationWidget):
    def __init__(self, manager, controller, allow_multiple_matrices=True):
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
        self.layout.setContentsMargins(20, 10, 10, 10)

        # Añadir configuración de dimensiones
        self._setup_dimension_config()

        # Configurar área de scroll
        self.scroll_area, self.scroll_content, self.scroll_layout = UIUtils.create_scrollable_area()
        
        # Añadir grid layout para matrices
        self.matrices_grid = QGridLayout()
        self.matrices_grid.setVerticalSpacing(30)
        self.matrices_grid.setHorizontalSpacing(50)
        self.scroll_layout.addLayout(self.matrices_grid)
        
        self.layout.addWidget(self.scroll_area)

        # Crear botones
        buttons_widget = self.create_buttons()
        self.layout.addWidget(buttons_widget)
        self.setLayout(self.layout)

        # Conectar señales
        self._connect_signals()
        
        # Inicializar matrices si es necesario
        if not hasattr(self, 'skip_initial_matrices'):
            self.update_matrix_tables()

    def _setup_dimension_config(self):
        """Configura los widgets de dimensión"""
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(20, 0, 0, 0)

        # Label y spinbox para dimensiones
        self.dim_label = QLabel("Dimensión de la matriz:" if not self.allow_multiple_matrices 
                               else "Dimensión de las matrices (n x n):")
        self.dim_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.dim_spinbox = create_int_spinbox(min_val=1, max_val=10, default_val=4)
        
        config_layout.addWidget(self.dim_label)
        config_layout.addWidget(self.dim_spinbox)
        config_layout.addSpacing(20)

        # Añadir control de cantidad si es necesario
        if self.allow_multiple_matrices:
            self._add_count_control(config_layout)

        config_layout.addStretch()
        self.layout.addWidget(config_widget)
        
    def _add_count_control(self, layout):
        """Añade control de cantidad de matrices"""
        self.matrix_count_label = QLabel("Cantidad de matrices:")
        self.matrix_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.matrix_count_spinbox = create_int_spinbox(min_val=2, max_val=10, default_val=2)
        
        layout.addWidget(self.matrix_count_label)
        layout.addWidget(self.matrix_count_spinbox)

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

        # Obtener el tamaño disponible del área de scroll
        available_width = self.scroll_area.viewport().width() - 20  # Margen de seguridad
        available_height = self.scroll_area.viewport().height() - 20
        spacing = self.matrices_grid.horizontalSpacing()

        # Calcular el número máximo de columnas que caben
        min_table_width = dimension * 50  # Ancho mínimo basado en celdas de 30px
        max_columns = max(1, available_width // (min_table_width + spacing))
        max_columns = min(max_columns, matrix_count)  # No más columnas que matrices

        # Calcular el tamaño de celda óptimo
        if max_columns > 0:
            cell_size_width = max(50, (available_width - (spacing * (max_columns - 1))) // (max_columns * dimension))
            
            # También considerar la altura disponible
            estimated_label_height = 20  # Altura estimada de la etiqueta
            rows_needed = (matrix_count + max_columns - 1) // max_columns
            cell_size_height = max(30, (available_height - (spacing * (rows_needed - 1) - estimated_label_height * rows_needed)) // (rows_needed * dimension))
            
            cell_size = min(cell_size_width, cell_size_height, 60)  # Usar el menor de los dos y limitar a 60px máximo
        else:
            cell_size = 60  # Valor por defecto

        self.tables = []  # Limpiar tablas previas

        # Crear las matrices en la cuadrícula
        for i in range(matrix_count):
            row = i // max_columns
            col = i % max_columns

            label_text = f"Matriz {chr(65 + i)}"
            table_data = MatrixTableComponent.create_table(dimension, dimension, label_text, cell_size)
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
            
            # Verificar que haya matrices suficientes
            if not matrices:
                raise ValueError("No hay matrices para operar.")
            
            # Enviar matrices al manager
            self.manager.matrices.clear()
            for matrix in matrices:
                self.manager.add_matrix(matrix)
                
            # Obtener la operación asociada
            operation_key = self._get_operation_key()
            
            # Ejecutar la operación
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

class OneMatrixOperationWidget(MatrixOperationWidget):
    """Clase base para operaciones con una sola matriz (ej. Transpuesta, Determinante)"""
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)
        self.skip_initial_matrices = True 