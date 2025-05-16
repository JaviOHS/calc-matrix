from ui.pages.matrix_page.operation_widgets.basic_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QTableWidget, QLabel, QTableWidgetItem
from utils.validators import is_valid_number

class MatrixSystemSolverWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        self.dim = 3
        self.skip_initial_matrices = True
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        super().setup_ui()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        self.dim_spinbox.valueChanged.connect(self.update_table)
        self.update_table()

    def update_table(self):
        self.dim = self.dim_spinbox.value()
        self._clear_previous_table()
        self._create_and_add_table()

    def _clear_previous_table(self):
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
        label_system = QLabel("Sistema de ecuaciones a · x = b")
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

        # Configurar el encabezado para no permitir redimensionamiento
        header = self.system_table.horizontalHeader()
        from PySide6.QtWidgets import QHeaderView  # Añade este import al inicio del archivo
        header.setSectionResizeMode(QHeaderView.Fixed)  # Bloquea el redimensionamiento
        
        # También puedes deshabilitar el encabezado completamente si lo prefieres
        # header.setDisabled(True)

        # Tamaño de celdas
        cell_size = 50
        header.setDefaultSectionSize(cell_size)
        self.system_table.verticalHeader().setDefaultSectionSize(cell_size)
        self.system_table.setFixedSize((self.dim + 1) * cell_size + 2, 
                                    (self.dim * cell_size) + header.sizeHint().height() + 2)
        self.system_table.setSelectionMode(QTableWidget.NoSelection)
        self.system_table.setFocusPolicy(Qt.NoFocus)

        import random

        for r in range(self.dim):
            for c in range(self.dim + 1):
                random_value = random.randint(1, 9) 
                item = QTableWidgetItem(str(random_value))
                item.setTextAlignment(Qt.AlignCenter)
                self.system_table.setItem(r, c, item)

        container_layout.addWidget(self.system_table, 0, Qt.AlignHCenter | Qt.AlignTop)
        self.scroll_layout.addWidget(container, alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.scroll_layout.addStretch()
    
    def validate_operation(self):
        for row in range(self.dim):
            for col in range(self.dim + 1):
                item = self.system_table.item(row, col)
                text = item.text() if item else ""
                try:
                    float(text)
                except (ValueError, TypeError):
                    return False, f"Valor inválido en fila {row+1}, columna {col+1}: '{text}'"
        return True, ""

    def collect_matrices(self):
        # Recolectar datos de la tabla
        matrix_data = []
        b_data = []
        
        for row in range(self.dim):
            row_data = []
            for col in range(self.dim + 1):  # +1 para incluir la columna de b
                item = self.system_table.item(row, col)
                value = item.text() if item else "0"
                if not is_valid_number(value):
                    raise ValueError(f"Valor inválido en fila {row+1}, columna {col+1}: '{value}'")
                
                if col < self.dim: # Los primeros 'dim' columnas son la matriz A, la última es b
                    row_data.append(float(value))
                else:
                    b_data.append([float(value)])  # b es una columna
            
            matrix_data.append(row_data)

        # Crear la matriz A (dim x dim) y la matriz B (dim x 1)
        A = Matrix(self.dim, self.dim, matrix_data)
        B = Matrix(self.dim, 1, b_data)
        
        return [A, B]
    
    def perform_operation(self):
        # Validar la operación
        is_valid, error_message = self.validate_operation()
        if not is_valid:
            self.show_message_dialog("🔴 ERROR", "#f44336", error_message)
            return

        # Recoger las matrices de la tabla
        matrices = self.collect_matrices()
        A, B = matrices[0], matrices[1]

        # Resolver el sistema de ecuaciones
        try:
            result = A.solve(B)
            self.show_result(result, "Sistema de ecuaciones resuelto", "Sistema de Ecuaciones")
        except ValueError as e:
            self.show_message_dialog("Error", str(e))
        except Exception as e:
            self.show_message_dialog("Error", f"Error inesperado: {str(e)}")
            