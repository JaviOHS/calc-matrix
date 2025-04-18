from ui.pages.matrix_page.operation_widgets.base_operation import MatrixOperationWidget
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QSpinBox, QPushButton, QHBoxLayout, QFormLayout
from model.matrix_model import Matrix
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QSizePolicy, QScrollArea

class MatrixSystemSolverWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        # Formulario de configuración
        config_widget = QWidget()
        config_layout = QFormLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Número de incógnitas:")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.dim_spinbox = QSpinBox()
        self.dim_spinbox.setAlignment(Qt.AlignCenter)
        self.dim_spinbox.setRange(2, 10)
        self.dim_spinbox.setValue(2)
        self.dim_spinbox.setObjectName("dim_spinbox")

        config_layout.addRow(label, self.dim_spinbox)
        self.layout.addWidget(config_widget)

        # Crear un widget contenedor para la tabla
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        table_layout.setAlignment(Qt.AlignCenter)  # Centrar la tabla dentro del contenedor

        # Tabla del sistema
        self.system_table = QTableWidget()
        self.system_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.system_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No scroll vertical
        self.system_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # No scroll horizontal
        self.system_table.setShowGrid(True)
        self.system_table.verticalHeader().setVisible(False)

        table_layout.addWidget(self.system_table)  # Añadir la tabla al layout centrado
        self.layout.addWidget(table_widget)  # Añadir el contenedor al layout principal

        # Botones
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.cancel_button = QPushButton("Cancelar")
        self.calculate_button = QPushButton("Resolver")

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.calculate_button)

        self.layout.addWidget(buttons_widget)
        self.setLayout(self.layout)

        # Conexiones
        self.dim_spinbox.valueChanged.connect(self.update_table)
        self.update_table()

    def update_table(self):
        dim = self.dim_spinbox.value()
        self.system_table.setRowCount(dim)
        self.system_table.setColumnCount(dim + 1)

        headers = [f"x{i+1}" for i in range(dim)] + ["= b"]
        self.system_table.setHorizontalHeaderLabels(headers)

        # Establecer tamaño de las celdas
        cell_size = 50
        self.system_table.horizontalHeader().setDefaultSectionSize(cell_size)
        self.system_table.verticalHeader().setDefaultSectionSize(cell_size)

        # Llenar la tabla con valores por defecto
        for r in range(dim):
            for c in range(dim + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.system_table.setItem(r, c, item)

        # Ajustar las filas y columnas para que se ajusten al contenido
        self.system_table.resizeColumnsToContents()
        self.system_table.resizeRowsToContents()

        # Asegúrate de que la tabla ocupe todo el espacio disponible
        self.system_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.system_table.updateGeometry()
        
    def validate_operation(self):
        dim = self.dim_spinbox.value()

        for row in range(dim):
            for col in range(dim + 1):
                item = self.system_table.item(row, col)
                if not item or not item.text().replace('.', '').replace('-', '').isdigit():
                    return False, f"Valor inválido en fila {row+1}, columna {col+1}"

        return True, ""

    def collect_matrices(self):
        dim = self.dim_spinbox.value()
        A = Matrix(dim, dim)
        b = Matrix(dim, 1)

        for row in range(dim):
            for col in range(dim):
                A.set_value(row, col, float(self.system_table.item(row, col).text()))
            b.set_value(row, 0, float(self.system_table.item(row, dim).text()))

        return [A, b]
