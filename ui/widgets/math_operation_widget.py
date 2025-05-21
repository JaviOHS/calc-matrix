from PySide6.QtWidgets import QWidget, QHBoxLayout
from utils.components.action_buttons import ActionButton

class MathOperationWidget(QWidget):
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
        buttons_layout.setContentsMargins(20, 0, 20, 0)
        buttons_layout.setSpacing(10)

        # Usar los botones predefinidos
        self.cancel_button = ActionButton.cancel(cancel_text)
        self.calculate_button = ActionButton.calculate(action_text)

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
        