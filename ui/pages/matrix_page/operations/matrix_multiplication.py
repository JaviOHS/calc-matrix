from ui.pages.matrix_page.operations.matrix_base_operation import MatrixBaseOp
from utils.layout.matrix_table import MatrixTableComponent
from utils.components.ui_utils import UIUtils
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from utils.components.two_row import TwoRowWidget
from utils.components.dimension_config_utils import DimensionConfigUtils

class MatrixMultiplicationWidget(MatrixBaseOp):
    def __init__(self, manager, controller):
        self.a_rows_spinbox = None
        self.a_cols_spinbox = None
        self.b_cols_spinbox = None
        self.tables = []
        self.skip_initial_matrices = True
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.two_row_widget = TwoRowWidget(row1_label="Dimensiones de Matrices", row2_label="Matrices para Multiplicación")
        self.two_row_widget.setContentsMargins(20, 0, 20, 0)
        
        main_layout.addWidget(self.two_row_widget)

        self._setup_custom_dimensions()
        self._setup_matrices_area()

        # Añadir botones
        buttons_widget = self.create_buttons()
        buttons_widget.setContentsMargins(20, 10, 20, 10)
        main_layout.addWidget(buttons_widget)

        # Conectar señales
        self._connect_signals()
        
        # Actualizar matrices iniciales
        self.update_matrix_tables()

    def _setup_custom_dimensions(self):
        """Configurar controles de dimensión específicos para multiplicación"""
        config_widget, self.a_rows_spinbox, self.a_cols_spinbox, self.b_cols_spinbox = \
            DimensionConfigUtils.create_multiplication_dimension_config()
        
        # Añadir a la primera fila del TwoRowWidget
        self.two_row_widget.add_to_row1(config_widget)

    def _setup_matrices_area(self):
        """Configurar el área de matrices para la multiplicación"""
        # Crear área de scroll y grid para matrices
        self.scroll_area, self.scroll_content, self.scroll_layout = UIUtils.create_scrollable_area()
        self.matrices_grid = QHBoxLayout()
        self.matrices_grid.setSpacing(30) # Espacio entre matrices
        self.scroll_layout.addLayout(self.matrices_grid)
        
        # Añadir a la segunda fila del TwoRowWidget
        self.two_row_widget.add_to_row2(self.scroll_area)

    def _connect_signals(self):
        """Conectar señales para actualizar cuando cambian las dimensiones"""
        self.a_rows_spinbox.valueChanged.connect(self.update_matrix_tables)
        self.a_cols_spinbox.valueChanged.connect(self.update_matrix_tables)
        self.b_cols_spinbox.valueChanged.connect(self.update_matrix_tables)
        self.scroll_area.viewport().installEventFilter(self)

    def update_matrix_tables(self):
        """Actualiza las tablas de matrices según las dimensiones especificadas"""
        # Limpiar matrices previas
        for i in reversed(range(self.matrices_grid.count())):
            item = self.matrices_grid.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Obtener dimensiones
        ar = self.a_rows_spinbox.value()
        ac = self.a_cols_spinbox.value()
        bc = self.b_cols_spinbox.value()

        # Crear tablas usando MatrixTableComponent
        self.tables = []
        
        # Crear tabla A
        table_a = MatrixTableComponent.create_table(ar, ac, "Matriz A", cell_size=50)
        self.tables.append(table_a)
        self.matrices_grid.addWidget(table_a["widget"])

        # Crear tabla B
        table_b = MatrixTableComponent.create_table(ac, bc, "Matriz B", cell_size=50)
        self.tables.append(table_b)
        self.matrices_grid.addWidget(table_b["widget"])

        # Actualizar la vista
        self.scroll_content.updateGeometry()
