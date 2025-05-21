from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from ui.widgets.base_page import BasePage
from ui.pages.matrix_page.operations.matrix_base_operation import MatrixBaseOp, OneMatrixOpWidget
from ui.pages.matrix_page.operations.matrix_multiplication import MatrixMultiplicationWidget
from ui.pages.matrix_page.operations.matrix_system_solver import MatrixSystemSolverWidget

class MatrixPage(BasePage):
    def __init__(self, navigate_callback=None, manager=MatrixManager()):
        self.controller = MatrixController(manager)
        
        super().__init__(navigate_callback, page_key="matrix", controller=self.controller, manager=manager)

        # Definir las operaciones disponibles
        self.operations = {
            "Suma": ("plus", MatrixBaseOp),
            "Resta": ("substract", MatrixBaseOp),
            "Multiplicación": ("multiplication", MatrixMultiplicationWidget),
            "División": ("division", MatrixBaseOp),
            "Determinante": ("determinant", OneMatrixOpWidget),
            "Inversa": ("reverse", OneMatrixOpWidget),
            "Transpuesta": ("transposed", OneMatrixOpWidget),
            "Sistema de Ecuaciones": ("system_solver", MatrixSystemSolverWidget),
            "Vectores y Valores Propios": ("eigenvalues", OneMatrixOpWidget),
        }

    def execute_current_operation(self):
        label_key = next((label for label, (op_key, _) in self.operations.items() if op_key == self.current_operation), None)
        
        if not label_key:
            error_msg = f"No se encontró el widget para la operación: {self.current_operation}"
            self.show_message_dialog("🔴 ERROR", "#f44336", error_msg)
            return

        widget = self.operation_widgets.get(label_key)
        try:
            matrices = widget.collect_matrices()
            self.manager.matrices.clear()
            
            for matrix in matrices:
                self.manager.add_matrix(matrix)

            result = self.controller.execute_operation(self.current_operation)
            self.show_result(result, f"{self.current_operation.capitalize()} realizada correctamente", label_key)

        except ValueError as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", str(e))

        except Exception as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"Error inesperado: {str(e)}")
            
    def show_result(self, result, message, operation_name=""):
        """Muestra el resultado de una operación matricial"""
        from ui.pages.matrix_page.matrix_result_handler import ResultHandler
        
        if ResultHandler.show_matrix_result(result, operation_name, self):
            return
                
        # Si el ResultHandler no pudo manejar el resultado, mostrar diálogo genérico
        self.show_message_dialog("🔵 RESULTADO GENÉRICO", "#1976d2", str(result))
