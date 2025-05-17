from ui.pages.matrix_page.matrix_operations.matrix_operation import MatrixOperationWidget
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHeaderView, QHBoxLayout
from utils.matrix_table import MatrixTableComponent
from utils.ui_utils import UIUtils
from utils.validators.matrix_validator import MatrixValidator
from utils.spinbox_utils import create_int_spinbox

class MatrixSystemSolverWidget(MatrixOperationWidget):
    def __init__(self, manager, controller):
        self.dim = 3
        self.skip_initial_matrices = True
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        # No llamamos a super().setup_ui() para evitar la creación de matrices estándar
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)
        
        self._setup_dimension_config() # Añadir configuración de dimensiones (reutilizando el método del padre)

        # Configurar área de scroll usando UIUtils
        self.scroll_area, self.scroll_content, self.scroll_layout = UIUtils.create_scrollable_area()
        self.layout.addWidget(self.scroll_area)
        
        # Crear botones (reutilizando el método del padre)
        buttons_widget = self.create_buttons()
        self.layout.addWidget(buttons_widget)

        # Conectar señales
        self.dim_spinbox.valueChanged.connect(self.update_table)
        
        # Crear tabla inicial
        self.update_table()

    def _setup_dimension_config(self):
        """Configura los widgets de dimensión con margen izquierdo consistente"""
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(32, 0, 0, 0)  # Asegurar margen izquierdo

        # Label y spinbox para dimensiones
        self.dim_label = QLabel("Dimensión del sistema (n x n):")
        self.dim_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.dim_spinbox = create_int_spinbox(min_val=1, max_val=10, default_val=3)

        config_layout.addWidget(self.dim_label)
        config_layout.addWidget(self.dim_spinbox)
        config_layout.addStretch()

        self.layout.addWidget(config_widget)

    def update_table(self):
        """Actualiza la tabla del sistema de ecuaciones basada en la dimensión actual"""
        self.dim = self.dim_spinbox.value()
        self._clear_previous_table()
        self._create_and_add_table()

    def _clear_previous_table(self):
        """Limpia cualquier tabla existente del layout"""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _create_and_add_table(self):
        """Crea y añade la tabla del sistema de ecuaciones"""
        # Crear contenedor para el sistema
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

        # Crear tabla con las dimensiones del sistema
        table_data = MatrixTableComponent.create_table(
            self.dim, 
            self.dim + 1,  # Una columna extra para b
            "", 
            cell_size=50,
            random_fill=True
        )
        
        self.system_table = table_data["table"]
        
        # Configurar cabeceras específicas para el sistema de ecuaciones
        headers = [f"x{i+1}" for i in range(self.dim)] + ["= b"]
        self.system_table.setHorizontalHeaderLabels(headers)
        self.system_table.horizontalHeader().setVisible(True)
        
        # Configurar el encabezado para no permitir redimensionamiento
        header = self.system_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)
        
        # Ajustar tamaño de la tabla
        cell_size = 50
        self.system_table.setFixedSize(
            (self.dim + 1) * cell_size + 2, 
            (self.dim * cell_size) + header.sizeHint().height() + 2
        )

        container_layout.addWidget(table_data["widget"], 0, Qt.AlignHCenter | Qt.AlignTop)
        self.scroll_layout.addWidget(container, alignment=Qt.AlignHCenter | Qt.AlignTop)
        self.scroll_layout.addStretch()

    def collect_matrices(self):
        """Recolecta las matrices A y B del sistema de ecuaciones"""
        try:
            # Validar la matriz completa
            all_values = MatrixValidator.validate_table_values(self.system_table, matrix_name="Sistema de ecuaciones")
            
            # Separar los datos en A y b
            matrix_data = []
            b_data = []
            
            for row in range(self.dim):
                row_data = all_values[row][:self.dim]  # Valores de A (primeras dim columnas)
                matrix_data.append(row_data)
                b_data.append([all_values[row][self.dim]])  # Valor de b (última columna)

            # Crear matrices A y B
            A = Matrix(self.dim, self.dim, matrix_data)
            B = Matrix(self.dim, 1, b_data)
            
            return [A, B]
        except ValueError as e:
            raise ValueError(str(e))
