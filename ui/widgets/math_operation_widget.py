from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class MathOperationWidget(QWidget):
    """Clase base para widgets de operaciones matemáticas"""
    def __init__(self, manager, controller, operation_type=None):
        super().__init__()
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type

    def setup_ui(self):
        self.create_buttons()
    
    def create_buttons(self, cancel_text="Cancelar", action_text="Calcular"):
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.cancel_button = QPushButton(cancel_text)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.calculate_button = QPushButton(action_text)
        self.calculate_button.setCursor(Qt.PointingHandCursor)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.calculate_button)
        return buttons_widget

    def validate_operation(self):
        """Valida si la operación puede realizarse"""
        raise NotImplementedError

    def perform_operation(self):
        """Ejecuta la operación y retorna el resultado"""
        raise NotImplementedError

    def cleanup(self):
        """Limpia los recursos de la operación"""
        self.manager.clear()
        