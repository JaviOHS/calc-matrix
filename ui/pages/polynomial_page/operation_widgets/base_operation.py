from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from PySide6.QtWidgets import QWidget

class PolynomialOperationWidget(QWidget):
    """Clase base para widgets de operaciones con polinomios"""
    def __init__(self, manager: PolynomialManager, controller: PolynomialController, operation_type=None):
        super().__init__()
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de la operación"""
        raise NotImplementedError
    
    def validate_operation(self):
        """Valida si la operación puede realizarse"""
        raise NotImplementedError
    
    def collect_polynomials(self):
        """Recolecta los polinomios ingresados"""
        raise NotImplementedError
    
    def cleanup(self):
        """Limpia los recursos de la operación"""
        self.manager.polynomials.clear()