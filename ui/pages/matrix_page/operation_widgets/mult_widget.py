from ui.pages.matrix_page.operation_widgets.matrix_op import MatrixSimpleOP
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QHBoxLayout, QSpinBox, QWidget, QTableWidgetItem

class MatrixMultiplicationWidget(MatrixSimpleOP):
    def __init__(self, manager, controller):
        self.a_rows = None
        self.a_cols = None
        self.b_cols = None
        self.tables = []
        self.skip_initial_matrices = True
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        super().setup_ui()
        # Ocultar elementos de dimensiones no necesarios
        self.dim_label.hide()
        self.dim_spinbox.hide()

        # Configuración de dimensiones específicas para multiplicación
        self.dim_config_widget = QWidget()
        config_layout = QHBoxLayout(self.dim_config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        # Crear spinboxes
        self.a_rows = QSpinBox()
        self.a_cols = QSpinBox()
        self.b_cols = QSpinBox()
        
        for spin in [self.a_rows, self.a_cols, self.b_cols]:
            spin.setRange(1, 10)
            spin.setValue(3)
            spin.setAlignment(Qt.AlignCenter)
            spin.setObjectName("dim_spinbox")

        # Añadir al layout existente (no crear uno nuevo)
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

        # Conexiones
        self.a_rows.valueChanged.connect(self.update_matrix_tables)
        self.a_cols.valueChanged.connect(self.update_matrix_tables)
        self.b_cols.valueChanged.connect(self.update_matrix_tables)

        self.update_matrix_tables()

    def update_matrix_tables(self):
        for i in reversed(range(self.matrices_grid.count())): # Limpiar el grid
            widget = self.matrices_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        ar = self.a_rows.value()
        ac = self.a_cols.value()
        bc = self.b_cols.value()

        self.tables = []

        # Tabla A
        table_a = self.create_table(ar, ac, "Matriz A")
        self.tables.append(table_a)

        # Tabla B
        table_b = self.create_table(ac, bc, "Matriz B")
        self.tables.append(table_b)

        # Añadir al grid
        self.matrices_grid.addWidget(table_a["widget"], 0, 0, Qt.AlignCenter)
        self.matrices_grid.addWidget(table_b["widget"], 0, 1, Qt.AlignCenter)

    def create_table(self, rows, cols, label_text):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-weight: bold;")

        table = QTableWidget()
        table.setRowCount(rows)
        table.setColumnCount(cols)
        table.setFixedSize(cols * 40 + 2, rows * 40 + 2)
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

        layout.addWidget(label)
        layout.addWidget(table, 0, Qt.AlignCenter)

        return {"widget": widget, "table": table}

    def validate_operation(self):
        for t in self.tables:
            table = t["table"]
            for r in range(table.rowCount()):
                for c in range(table.columnCount()):
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

        table_a = self.tables[0]["table"]
        table_b = self.tables[1]["table"]

        for r in range(ar):
            for c in range(ac):
                A.set_value(r, c, float(table_a.item(r, c).text()))

        for r in range(ac):
            for c in range(bc):
                B.set_value(r, c, float(table_b.item(r, c).text()))

        return [A, B]

    def perform_operation(self):
        matrices = self.collect_matrices()
        result = self.controller.multiply(matrices[0], matrices[1])
        return result