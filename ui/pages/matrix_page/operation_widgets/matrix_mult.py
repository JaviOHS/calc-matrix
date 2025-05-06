from ui.pages.matrix_page.operation_widgets.basic_operation import MatrixOperationWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSpinBox, QWidget, QHBoxLayout, QSizePolicy

class MatrixMultiplicationWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        self.a_rows = None
        self.a_cols = None
        self.b_cols = None
        self.tables = []
        self.skip_initial_matrices = True
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        super().setup_ui()
        # Crear widgets para la configuración específica de la multiplicación
        self.dim_config_widget = QWidget()
        config_layout = QHBoxLayout(self.dim_config_widget)
        config_layout.setContentsMargins(20, 0, 0, 0)

        # Crear spinboxes para dimensiones de las matrices
        self.a_rows = QSpinBox()
        self.a_cols = QSpinBox()
        self.b_cols = QSpinBox()

        for spin in [self.a_rows, self.a_cols, self.b_cols]:
            spin.setRange(1, 10)
            spin.setValue(3)  # Valor inicial
            spin.setAlignment(Qt.AlignCenter)
            spin.setObjectName("dim_spinbox")

        # Añadir los spinboxes al layout
        config_layout.addWidget(QLabel("Filas de A:"))
        config_layout.addWidget(self.a_rows)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Columnas de A (y filas de B):"))
        config_layout.addWidget(self.a_cols)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Columnas de B:"))
        config_layout.addWidget(self.b_cols)
        config_layout.addStretch()

        # Reemplazar el widget de configuración original
        original_config_widget = self.layout.itemAt(0).widget()
        self.layout.replaceWidget(original_config_widget, self.dim_config_widget)
        original_config_widget.deleteLater()

        # Conectar las señales para actualizar las tablas
        self.a_rows.valueChanged.connect(self.update_matrix_tables)
        self.a_cols.valueChanged.connect(self.update_matrix_tables)
        self.b_cols.valueChanged.connect(self.update_matrix_tables)

        # Llamar a la función de actualización de tablas
        self.update_matrix_tables()

    def update_matrix_tables(self):
        # Limpiar matrices previas
        for i in reversed(range(self.matrices_grid.count())):
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Obtener las dimensiones de las matrices
        ar = self.a_rows.value()  # Filas de A
        ac = self.a_cols.value()  # Columnas de A (Filas de B)
        bc = self.b_cols.value()  # Columnas de B

        self.tables = []

        # Crear las tablas utilizando el método heredado de la clase base
        table_a = self.create_table(ar, ac, "Matriz A", cell_size=40)
        self.tables.append(table_a)

        table_b = self.create_table(ac, bc, "Matriz B", cell_size=40)
        self.tables.append(table_b)

        # Añadir las tablas al grid layout de la interfaz
        self.matrices_grid.addWidget(table_a["widget"], 0, 0, Qt.AlignCenter)
        self.matrices_grid.addWidget(table_b["widget"], 0, 1, Qt.AlignCenter)

        # Redimensionar las tablas según el tamaño del área visible
        self.update_scroll_area()

    def update_scroll_area(self):
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def perform_operation(self):
        matrices = self.collect_matrices()  # Recoger las matrices de las tablas
        result = self.controller.multiply(matrices[0], matrices[1])  # Realizar la multiplicación
        return result
