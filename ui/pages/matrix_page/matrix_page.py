from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from model.matrix_model import Matrix
from ui.widgets.base_page import BasePage
from ui.pages.matrix_page.operation_widgets.basic_operation import MatrixOperationWidget, MatrixDeterminantWidget, MatrixInverseWidget
from ui.pages.matrix_page.operation_widgets.matrix_mult import MatrixMultiplicationWidget
from ui.pages.matrix_page.operation_widgets.solver_sys_widget import MatrixSystemSolverWidget
from ui.dialogs.matrix_result_dialog import MatrixResultDialog

class MatrixPage(BasePage):
    def __init__(self, navigate_callback=None, manager=MatrixManager()):
        self.controller = MatrixController(manager)
        
        super().__init__(navigate_callback, page_key="matrix", controller=self.controller, manager=manager)

        # Definir las operaciones disponibles
        self.operations = {
            "Suma": ("suma", MatrixOperationWidget),
            "Resta": ("resta", MatrixOperationWidget),
            "Multiplicación": ("multiplicacion", MatrixMultiplicationWidget),
            "División": ("division", MatrixOperationWidget),
            "Determinante": ("determinante", MatrixDeterminantWidget),
            "Inversa": ("inversa", MatrixInverseWidget),
            "Sistema de Ecuaciones": ("sistema", MatrixSystemSolverWidget)
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
        if isinstance(result, list):
            if operation_name == "Determinante":
                for matrix_name, det_val in result:
                    result_matrix = Matrix(1, 1)
                    result_matrix.set_value(0, 0, det_val)
                    dialog = MatrixResultDialog(result_matrix, operation=operation_name, parent=self)
                    dialog.exec()
                return

            if operation_name == "Inversa":
                for matrix_name, inverse_matrix in result:
                    if isinstance(inverse_matrix, Matrix):  # Si es una matriz, muestra la inversa
                        dialog = MatrixResultDialog(inverse_matrix, operation=operation_name, parent=self)
                        dialog.exec()
                    else:
                        self.show_message_dialog("🔴 ERROR", "#f44336", inverse_matrix)
                return

        if isinstance(result, Matrix):
            dialog = MatrixResultDialog(result, operation=operation_name, parent=self)
            dialog.exec()
