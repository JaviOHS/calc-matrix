from ui.pages.matrix_page.operation_widgets.base_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QSpinBox, QPushButton, QHBoxLayout, QFormLayout, QWidget, QTableWidgetItem, QSizePolicy, QScrollArea

class MatrixSystemSolverWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        # Formulario de configuración (sin cambios)
        config_widget = QWidget()
        config_layout = QFormLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(20)

        label = QLabel("Número de incógnitas:")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.dim_spinbox = QSpinBox()
        self.dim_spinbox.setAlignment(Qt.AlignCenter)
        self.dim_spinbox.setRange(2, 10)
        self.dim_spinbox.setValue(3)
        self.dim_spinbox.setObjectName("dim_spinbox")
        self.dim_spinbox.setMaximumWidth(40)

        config_layout.addRow(label, self.dim_spinbox)
        self.layout.addWidget(config_widget)

        # --- Área de scroll para la tabla (nuevo) ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Contenedor principal para la tabla
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)  # Alinear el contenido arriba

        # Tabla del sistema
        self.system_table = QTableWidget()
        self.system_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.system_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.system_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.system_table.setShowGrid(True)
        self.system_table.verticalHeader().setVisible(False)

        # Añadir la tabla al layout (centrada horizontalmente)
        self.scroll_layout.addWidget(self.system_table, 0, Qt.AlignHCenter)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # Botones (sin cambios)
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

        # Limpiar el contenido anterior del scroll_layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Crear un widget contenedor para el título y la tabla
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        container_layout.setAlignment(Qt.AlignTop)  # Alinear el contenido arriba

        # Añadir el título
        label_system = QLabel("Sistema de ecuaciones a * x = b")
        label_system.setAlignment(Qt.AlignCenter)
        label_system.setStyleSheet("font-weight: bold;")
        container_layout.addWidget(label_system)

        # Configurar la tabla
        self.system_table = QTableWidget()
        self.system_table.setRowCount(dim)
        self.system_table.setColumnCount(dim + 1)
        self.system_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.system_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.system_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.system_table.setShowGrid(True)
        self.system_table.verticalHeader().setVisible(False)

        headers = [f"x{i+1}" for i in range(dim)] + ["= b"]
        self.system_table.setHorizontalHeaderLabels(headers)

        # Tamaño de celdas
        cell_size = 40
        self.system_table.horizontalHeader().setDefaultSectionSize(cell_size)
        self.system_table.verticalHeader().setDefaultSectionSize(cell_size)

        # Calcular tamaño total de la tabla
        table_width = (dim + 1) * cell_size + 2
        header_height = self.system_table.horizontalHeader().sizeHint().height()
        table_height = (dim * cell_size) + header_height + 2
        self.system_table.setFixedSize(table_width, table_height)

        # Llenar la tabla con valores por defecto
        for r in range(dim):
            for c in range(dim + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.system_table.setItem(r, c, item)

        # Añadir la tabla al contenedor (centrada horizontalmente)
        container_layout.addWidget(self.system_table, 0, Qt.AlignHCenter | Qt.AlignTop)

        # Añadir el contenedor al área de scroll
        self.scroll_layout.addWidget(container, alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.scroll_layout.addStretch()  # Esto empuja el contenido hacia arriba  
    
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
