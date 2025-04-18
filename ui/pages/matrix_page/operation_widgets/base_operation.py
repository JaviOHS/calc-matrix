from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from PySide6.QtWidgets import QWidget

"""Clase base para widgets de operaciones específicas"""
class MatrixOperationWidget(QWidget):
    def __init__(self, manager: MatrixManager, controller: MatrixController, allow_multiple_matrices=True):
        super().__init__()
        self.manager = manager
        self.controller = controller
        self.allow_multiple_matrices = allow_multiple_matrices
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de la operación"""
        raise NotImplementedError
    
    def get_config_values(self):
        """Obtiene los valores de configuración de la operación"""
        raise NotImplementedError
    
    def validate_operation(self):
        """Valida si la operación puede realizarse"""
        raise NotImplementedError
    
    def perform_operation(self):
        """Ejecuta la operación y retorna el resultado"""
        raise NotImplementedError
    
    def cleanup(self):
        """Limpia los recursos de la operación"""
        self.manager.matrices.clear()