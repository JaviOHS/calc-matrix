from ui.pages.matrix_page.operations.matrix_base_operation import MatrixBaseOp
from model.matrix_model import Matrix
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout
from utils.validators.matrix_validator import MatrixValidator
from utils.components.ui_utils import UIUtils
from utils.components.equation_system_utils import EquationSystemUtils
from utils.components.two_row import TwoRowWidget
from utils.components.dimension_config_utils import DimensionConfigUtils

class MatrixSystemSolverWidget(MatrixBaseOp):
    def __init__(self, manager, controller):
        self.dim = 3
        self.skip_initial_matrices = True
        super().__init__(manager, controller, allow_multiple_matrices=False)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.two_row_widget = TwoRowWidget(row1_label="Configuración del Sistema",  row2_label="Sistema de Ecuaciones a · x = b")
        self.two_row_widget.setContentsMargins(20, 0, 20, 0)
        
        main_layout.addWidget(self.two_row_widget)

        self._setup_dimension_config()
        self._setup_system_area()

        # Crear botones
        buttons_widget = self.create_buttons()
        buttons_widget.setContentsMargins(20, 10, 20, 10)
        main_layout.addWidget(buttons_widget)

        # Conectar señales
        self.dim_spinbox.valueChanged.connect(self.update_table)
        
        # Crear tabla inicial
        self.update_table()

    def _setup_dimension_config(self):
        """Configura los widgets de dimensión"""
        config_widget, self.dim_spinbox, _ = DimensionConfigUtils.create_dimension_config(allow_multiple_matrices=False)
        self.two_row_widget.add_to_row1(config_widget)

    def _setup_system_area(self):
        """Configura el área del sistema de ecuaciones"""
        self.scroll_area, self.scroll_content, self.scroll_layout = UIUtils.create_scrollable_area()
        self.two_row_widget.add_to_row2(self.scroll_area)

    def update_table(self):
        """Actualiza la tabla del sistema de ecuaciones"""
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
        system_data = EquationSystemUtils.create_equation_system_widget(self.dim)
        self.system_table = system_data["table"]
        self.scroll_layout.addWidget(
            system_data["container"], 
            alignment=Qt.AlignHCenter | Qt.AlignTop
        )
        self.scroll_layout.addStretch()

    def collect_matrices(self):
        """Recolecta las matrices A y B del sistema de ecuaciones"""
        try:
            all_values = MatrixValidator.validate_table_values(self.system_table, matrix_name="Sistema de ecuaciones")
            
            matrix_data = [] # Separar los datos en A y b
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
