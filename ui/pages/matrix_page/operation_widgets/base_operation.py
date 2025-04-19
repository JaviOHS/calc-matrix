from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from widgets.math_operation_widget import MathOperationWidget

class MatrixOperationWidget(MathOperationWidget):
    def __init__(self, manager: MatrixManager, controller: MatrixController, allow_multiple_matrices=True):
        self.manager = manager
        self.controller = controller
        self.allow_multiple_matrices = allow_multiple_matrices
        super().__init__(manager, controller, operation_type="matrix")
