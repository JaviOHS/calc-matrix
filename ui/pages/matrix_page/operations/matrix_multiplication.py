from ui.pages.matrix_page.operations.base_operation import MatrixOperationWidget
from utils.layout.matrix_table import MatrixTableComponent
from utils.components.ui_utils import UIUtils
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout
from utils.components.spinbox_utils import create_int_spinbox

class MatrixMultiplicationWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        # Configuración inicial antes de llamar al constructor padre
        self.a_rows = None
        self.a_cols = None
        self.b_cols = None
        self.tables = []
        self.skip_initial_matrices = True  # Evita crear matrices iniciales en el constructor padre
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        # Configuración básica del layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 10, 10, 10)
        
        self._setup_custom_dimensions() # Creamos control de dimensiones personalizado

        # Configurar área de scroll usando UIUtils
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

        # Conectar señales para actualizar cuando cambian las dimensiones
        self.a_rows.valueChanged.connect(self.update_matrix_tables)
        self.a_cols.valueChanged.connect(self.update_matrix_tables)
        self.b_cols.valueChanged.connect(self.update_matrix_tables)
        self.scroll_area.viewport().installEventFilter(self)

        # Actualizar tablas por primera vez
        self.update_matrix_tables()

    def _setup_custom_dimensions(self):
        """Configurar controles de dimensión específicos para multiplicación"""
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(20, 0, 0, 0)

        # Spinboxes para dimensiones específicas de multiplicación
        self.a_rows = create_int_spinbox(min_val=1, max_val=10, default_val=4)
        self.a_cols = create_int_spinbox(min_val=1, max_val=10, default_val=3)
        self.b_cols = create_int_spinbox(min_val=1, max_val=10, default_val=4)

        # Añadir elementos al layout
        config_layout.addWidget(QLabel("Filas de A:"))
        config_layout.addWidget(self.a_rows)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Columnas de A (y filas de B):"))
        config_layout.addWidget(self.a_cols)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Columnas de B:"))
        config_layout.addWidget(self.b_cols)
        config_layout.addStretch()

        self.layout.addWidget(config_widget)

    def update_matrix_tables(self):
        """Actualiza las tablas de matrices según las dimensiones especificadas"""
        # Limpiar matrices previas
        for i in reversed(range(self.matrices_grid.count())):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Obtener dimensiones
        ar = self.a_rows.value()
        ac = self.a_cols.value()
        bc = self.b_cols.value()

        # Crear tablas usando MatrixTableComponent
        self.tables = []
        
        # Crear tabla A
        table_a = MatrixTableComponent.create_table(ar, ac, "Matriz A", cell_size=50)
        self.tables.append(table_a)
        
        # Crear tabla B
        table_b = MatrixTableComponent.create_table(ac, bc, "Matriz B", cell_size=50)
        self.tables.append(table_b)

        # Añadir tablas al grid layout
        self.matrices_grid.addWidget(table_a["widget"], 0, 0, Qt.AlignCenter)
        self.matrices_grid.addWidget(table_b["widget"], 0, 1, Qt.AlignCenter)

        # Actualizar la vista
        self.scroll_content.updateGeometry()
