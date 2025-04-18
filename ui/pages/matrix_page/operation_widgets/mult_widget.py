from ui.pages.matrix_page.operation_widgets.base_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QSpinBox, QPushButton, QHBoxLayout, QWidget, QTableWidgetItem, QVBoxLayout, QSpinBox, QScrollArea, QWidget, QTableWidget, QLabel, QPushButton, QHBoxLayout, QTableWidgetItem, QGridLayout, QSizePolicy

class MatrixMultiplicationWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        # Configuración de dimensiones
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        self.a_rows = QSpinBox()
        self.a_cols = QSpinBox()
        self.b_cols = QSpinBox()
        for spin in [self.a_rows, self.a_cols, self.b_cols]:
            spin.setRange(1, 10)
            spin.setValue(2)
            spin.setObjectName("dim_spinbox")
            spin.setAlignment(Qt.AlignCenter) # Aplicar centrado a todos
            # spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred) # Expandir horizontalmente

        config_layout.addWidget(QLabel("Filas de A:"), alignment=Qt.AlignRight)
        config_layout.addWidget(self.a_rows)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Columnas de A (y filas de B):"), alignment=Qt.AlignRight)
        config_layout.addWidget(self.a_cols)
        config_layout.addSpacing(20)
        config_layout.addWidget(QLabel("Columnas de B:"), alignment=Qt.AlignRight)
        config_layout.addWidget(self.b_cols)
        config_layout.addStretch()

        self.layout.addWidget(config_widget)

        #  Área de scroll principal
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        # Grid para matrices (2 por fila)
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
        self.calculate_button = QPushButton("Multiplicar")

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.calculate_button)

        self.layout.addWidget(buttons_widget)
        self.setLayout(self.layout)

        # --- Conexiones ---
        self.a_rows.valueChanged.connect(self.update_tables)
        self.a_cols.valueChanged.connect(self.update_tables)
        self.b_cols.valueChanged.connect(self.update_tables)

        self.update_tables()

    def update_tables(self):
        ar = self.a_rows.value()
        ac = self.a_cols.value()
        bc = self.b_cols.value()

        # Limpiar el grid existente
        for i in reversed(range(self.matrices_grid.count())): 
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        cell_size = 40
        size_a = QSize(ac * cell_size + 2, ar * cell_size + 2)
        size_b = QSize(bc * cell_size + 2, ac * cell_size + 2)

        # Crear y agregar matriz A
        widget_a = QWidget()
        layout_a = QVBoxLayout(widget_a)
        layout_a.setContentsMargins(0, 0, 0, 0)
        layout_a.setSpacing(5)

        label_a = QLabel("Matriz A")
        label_a.setAlignment(Qt.AlignCenter)
        label_a.setStyleSheet("font-weight: bold;")

        self.table_a = QTableWidget()
        self.setup_table(self.table_a, ar, ac, size_a)

        layout_a.addWidget(label_a)
        layout_a.addWidget(self.table_a, 0, Qt.AlignCenter)

        # Crear y agregar matriz B
        widget_b = QWidget()
        layout_b = QVBoxLayout(widget_b)
        layout_b.setContentsMargins(0, 0, 0, 0)
        layout_b.setSpacing(5)

        label_b = QLabel("Matriz B")
        label_b.setAlignment(Qt.AlignCenter)
        label_b.setStyleSheet("font-weight: bold;")

        self.table_b = QTableWidget()
        self.setup_table(self.table_b, ac, bc, size_b)

        layout_b.addWidget(label_b)
        layout_b.addWidget(self.table_b, 0, Qt.AlignCenter)

        # Agregar al grid
        self.matrices_grid.addWidget(widget_a, 0, 0, Qt.AlignCenter)
        self.matrices_grid.addWidget(widget_b, 0, 1, Qt.AlignCenter)

    def setup_table(self, table, rows, cols, size: QSize):
        table.clear()
        table.setRowCount(rows)
        table.setColumnCount(cols)
        table.setFixedSize(size)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.horizontalHeader().setDefaultSectionSize(40)
        table.verticalHeader().setDefaultSectionSize(40)

        for r in range(rows):
            for c in range(cols):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(r, c, item)

    def validate_operation(self):
        ar = self.a_rows.value()
        ac = self.a_cols.value()
        bc = self.b_cols.value()

        for table, rows, cols in [(self.table_a, ar, ac), (self.table_b, ac, bc)]:
            for r in range(rows):
                for c in range(cols):
                    item = table.item(r, c)
                    if not item or not item.text().replace('.', '').replace('-', '').isdigit():
                        return False, f"Valor inválido en la matriz en fila {r+1}, columna {c+1}"
        return True, ""

    def collect_matrices(self):
        ar = self.a_rows.value()
        ac = self.a_cols.value()
        bc = self.b_cols.value()

        A = Matrix(ar, ac)
        B = Matrix(ac, bc)

        for r in range(ar):
            for c in range(ac):
                A.set_value(r, c, float(self.table_a.item(r, c).text()))

        for r in range(ac):
            for c in range(bc):
                B.set_value(r, c, float(self.table_b.item(r, c).text()))

        return [A, B]
