from PySide6.QtWidgets import QSizePolicy
from utils.layout.matrix_table import MatrixTableComponent
from utils.components.matrix_item_delegate import MatrixItemDelegate

class MatrixGridUtils:
    @staticmethod
    def calculate_matrix_layout(scroll_area, dimension, matrix_count, spacing=15):
        """Calcula el layout óptimo para las matrices"""
        available_width = scroll_area.viewport().width() - 20
        available_height = scroll_area.viewport().height() - 20
        
        min_table_width = dimension * 50
        max_columns = max(1, available_width // (min_table_width + spacing))
        max_columns = min(max_columns, matrix_count)
        
        # Calcular tamaño de celda óptimo
        if max_columns > 0:
            cell_size_width = max(50, (available_width - (spacing * (max_columns - 1))) // (max_columns * dimension))
            
            estimated_label_height = 20
            rows_needed = (matrix_count + max_columns - 1) // max_columns
            cell_size_height = max(30, (available_height - (spacing * (rows_needed - 1) - estimated_label_height * rows_needed)) // (rows_needed * dimension))
            
            cell_size = min(cell_size_width, cell_size_height, 60)
        else:
            cell_size = 50
            
        return max_columns, cell_size

    @staticmethod
    def create_matrix_widget(dimension, index, cell_size):
        """Crea un widget de matriz individual"""
        label_text = f"Matriz {chr(65 + index)}"
        table_data = MatrixTableComponent.create_table(dimension, dimension, label_text, cell_size)
        widget = table_data["widget"]
        
        # Configurar el delegado personalizado para la tabla
        delegate = MatrixItemDelegate()
        table_data["table"].setItemDelegate(delegate)
        
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        widget.setMinimumWidth(dimension * 30)
        widget.setMinimumHeight(dimension * 30 + table_data["label"].sizeHint().height())
        
        return table_data