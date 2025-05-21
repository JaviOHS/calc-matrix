from PySide6.QtWidgets import QSizePolicy, QScrollArea, QWidget, QVBoxLayout, QGridLayout
from PySide6.QtCore import Qt

class UIUtils:
    @staticmethod
    def create_scrollable_area():
        """Crea un área de desplazamiento configurable"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(scroll_content)
        
        return scroll_area, scroll_content, scroll_layout
    
    @staticmethod
    def calculate_grid_layout(total_items, available_width, min_item_width, spacing):
        """Calcula la disposición óptima de una cuadrícula"""
        max_columns = max(1, available_width // (min_item_width + spacing))
        max_columns = min(max_columns, total_items)
        rows_needed = (total_items + max_columns - 1) // max_columns
        
        return max_columns, rows_needed
    
    @staticmethod
    def create_matrix_grid_area(dimension, matrix_count, cell_size=60):
        """
        Crea un área de scroll con una cuadrícula optimizada para matrices
        
        Args:
            dimension (int): Dimensión de las matrices
            matrix_count (int): Número de matrices
            cell_size (int): Tamaño base de cada celda
        
        Returns:
            tuple: (scroll_area, matrices_grid, tables_list)
        """
        # Crear área scrollable base
        scroll_area, scroll_content, scroll_layout = UIUtils.create_scrollable_area()
        
        # Configurar grid para matrices
        matrices_grid = QGridLayout()
        matrices_grid.setVerticalSpacing(30)
        matrices_grid.setHorizontalSpacing(50)
        scroll_layout.addLayout(matrices_grid)
        
        # Configurar márgenes y espaciado
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        matrices_grid.setSpacing(15)
        
        return scroll_area, matrices_grid
