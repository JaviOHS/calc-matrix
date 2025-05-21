from PySide6.QtWidgets import QWidget, QHBoxLayout
from utils.components.spinbox_utils import create_int_spinbox

class DimensionConfigUtils:
    @staticmethod
    def create_dimension_config(allow_multiple_matrices=True):
        """Crea el widget de configuración de dimensiones"""
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)

        dimension_label = "📐 Dimensión de la matriz:" if not allow_multiple_matrices else "📐 Dimensión de las matrices (n x n):"
        dimension_container = create_int_spinbox(min_val=1, max_val=10, default_val=4, width=70, label_text=dimension_label)
        
        config_layout.addWidget(dimension_container)
        config_layout.addSpacing(25)

        matrix_count_container = None
        if allow_multiple_matrices:
            matrix_count_container = create_int_spinbox(
                min_val=2, 
                max_val=10, 
                default_val=2, 
                width=70,
                label_text="🔢 Cantidad de matrices:"
            )
            config_layout.addWidget(matrix_count_container)

        config_layout.addStretch()
        
        return config_widget, dimension_container.spinbox, matrix_count_container.spinbox if matrix_count_container else None

    @staticmethod
    def create_multiplication_dimension_config():
        """Creates dimension configuration specifically for matrix multiplication"""
        config_widget = QWidget()
        config_layout = QHBoxLayout(config_widget)
        config_layout.setContentsMargins(10, 5, 10, 5)
        config_layout.setSpacing(25)  # Espaciado uniforme entre widgets

        a_rows = create_int_spinbox(
            min_val=1,
            max_val=10,
            default_val=4,
            label_text="🔢 Filas de A:"
        )
        
        a_cols = create_int_spinbox(
            min_val=1,
            max_val=10,
            default_val=4,
            label_text="🔄 Columnas A/Filas B:"
        )
        
        b_cols = create_int_spinbox(
            min_val=1,
            max_val=10,
            default_val=4,
            label_text="📊 Columnas de B:"
        )

        config_layout.addWidget(a_rows)
        config_layout.addWidget(a_cols)
        config_layout.addWidget(b_cols)
        config_layout.addStretch(1)

        return config_widget, a_rows.spinbox, a_cols.spinbox, b_cols.spinbox