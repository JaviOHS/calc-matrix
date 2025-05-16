from PySide6.QtWidgets import QSizePolicy, QScrollArea, QWidget, QVBoxLayout
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
    