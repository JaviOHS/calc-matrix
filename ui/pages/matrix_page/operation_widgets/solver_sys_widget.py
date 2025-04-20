from ui.pages.matrix_page.operation_widgets.base_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QSpinBox, QWidget, QTableWidgetItem, QSizePolicy, QScrollArea, QHeaderView

class MatrixSystemSolverWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        super().__init__(manager, controller, allow_multiple_matrices=False)
        self.dim = 3  # Valor por defecto para la dimensión
        self.system_table = None
        self.scroll_layout = None
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self._setup_config_ui()
        self._setup_scroll_area()

        buttons_widget = self.create_buttons()
        self.layout.addWidget(buttons_widget)

        self.setLayout(self.layout)

        self.dim_spinbox.valueChanged.connect(self.update_table)
        self.update_table()

    def _setup_config_ui(self):
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Número de incógnitas:")
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.dim_spinbox = QSpinBox()
        self.dim_spinbox.setAlignment(Qt.AlignCenter)
        self.dim_spinbox.setRange(2, 10)
        self.dim_spinbox.setValue(self.dim)
        self.dim_spinbox.setObjectName("dim_spinbox")
        self.dim_spinbox.setMaximumWidth(60)

        config_layout.addWidget(label)
        config_layout.addWidget(self.dim_spinbox)
        config_layout.addStretch()

        self.layout.addWidget(config_widget)

    def _setup_scroll_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

    def update_table(self):
        self.dim = self.dim_spinbox.value()

        # Limpiar contenido anterior
        self._clear_previous_table()

        # Crear y agregar la nueva tabla
        self._create_and_add_table()

    def _clear_previous_table(self):
        # Limpiar el contenido anterior del scroll_layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _create_and_add_table(self):
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(5)
        container_layout.setAlignment(Qt.AlignTop)

        # Añadir el título
        label_system = QLabel("Sistema de ecuaciones a * x = b")
        label_system.setAlignment(Qt.AlignCenter)
        label_system.setStyleSheet("font-weight: bold;")
        container_layout.addWidget(label_system)

        # Crear y configurar la tabla
        self.system_table = QTableWidget()
        self.system_table.setRowCount(self.dim)
        self.system_table.setColumnCount(self.dim + 1)
        self.system_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.system_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.system_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.system_table.setShowGrid(True)
        self.system_table.verticalHeader().setVisible(False)

        headers = [f"x{i+1}" for i in range(self.dim)] + ["= b"]
        self.system_table.setHorizontalHeaderLabels(headers)

        # Tamaño de celdas
        cell_size = 50
        self.system_table.horizontalHeader().setDefaultSectionSize(cell_size)
        self.system_table.verticalHeader().setDefaultSectionSize(cell_size)
        
        # Configuración clave para deshabilitar el redimensionamiento
        self.system_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Deshabilita el redimensionamiento
        self.system_table.horizontalHeader().setSectionsClickable(False)  # Deshabilita la interacción con los encabezados
        self.system_table.horizontalHeader().setHighlightSections(False)  # Elimina el resaltado al pasar el mouse

        # Calcular tamaño total de la tabla
        table_width = (self.dim + 1) * cell_size + 2
        header_height = self.system_table.horizontalHeader().sizeHint().height()
        table_height = (self.dim * cell_size) + header_height + 2
        self.system_table.setFixedSize(table_width, table_height)
        self.system_table.setSelectionMode(QTableWidget.NoSelection)  # No permite selección alguna
        self.system_table.setFocusPolicy(Qt.NoFocus)  # Elimina el rectángulo de enfoque

        # Llenar la tabla con valores por defecto
        for r in range(self.dim):
            for c in range(self.dim + 1):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                self.system_table.setItem(r, c, item)

        # Añadir la tabla al contenedor
        container_layout.addWidget(self.system_table, 0, Qt.AlignHCenter | Qt.AlignTop)

        # Añadir el contenedor al área de scroll
        self.scroll_layout.addWidget(container, alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.scroll_layout.addStretch()

    def validate_operation(self):
        for row in range(self.dim):
            for col in range(self.dim + 1):
                item = self.system_table.item(row, col)
                if not item or not item.text().replace('.', '').replace('-', '').isdigit():
                    return False, f"Valor inválido en fila {row+1}, columna {col+1}"

        return True, ""

    def collect_matrices(self):
        A = Matrix(self.dim, self.dim)
        b = Matrix(self.dim, 1)

        for row in range(self.dim):
            for col in range(self.dim):
                A.set_value(row, col, float(self.system_table.item(row, col).text()))
            b.set_value(row, 0, float(self.system_table.item(row, self.dim).text()))

        return [A, b]
