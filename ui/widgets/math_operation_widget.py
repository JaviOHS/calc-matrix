from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
from utils.resources import resource_path
from utils.icon_utils import colored_svg_icon

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
        buttons_layout.setSpacing(16)

        # Botón Cancelar
        self.cancel_button = QPushButton(cancel_text)
        self.cancel_button.setObjectName("ctaButton")
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_icon = colored_svg_icon(resource_path("assets/icons/go.svg"), QColor(28, 44, 66))
        self.cancel_button.setIcon(cancel_icon)
        self.cancel_button.setIconSize(QSize(20, 20))

        # Botón Calcular
        self.calculate_button = QPushButton(action_text)
        self.calculate_button.setObjectName("ctaButton")
        self.calculate_button.setCursor(Qt.PointingHandCursor)
        calc_icon = colored_svg_icon(resource_path("assets/icons/calculator.svg"), QColor(28, 44, 66))
        self.calculate_button.setIcon(calc_icon)
        self.calculate_button.setIconSize(QSize(20, 20))

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
        