from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from model.matrix_model import Matrix
from ui.widgets.base_page_widget import BaseOperationPage
from ui.pages.matrix_page.operation_widgets.basic_operation import MatrixOperationWidget, MatrixDeterminantWidget, MatrixInverseWidget
from ui.pages.matrix_page.operation_widgets.matrix_mult import MatrixMultiplicationWidget
from ui.pages.matrix_page.operation_widgets.solver_sys_widget import MatrixSystemSolverWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from ui.dialogs.matrix_result_dialog import MatrixResultDialog

class MatrixPage(BaseOperationPage):
    def __init__(self, manager: MatrixManager):
        self.controller = MatrixController(manager)

        operations = {
            "Suma": ("suma", MatrixOperationWidget),
            "Resta": ("resta", MatrixOperationWidget),
            "Multiplicación": ("multiplicacion", MatrixMultiplicationWidget),
            "División": ("division", MatrixOperationWidget),
            "Determinante": ("determinante", MatrixDeterminantWidget),
            "Inversa": ("inversa", MatrixInverseWidget),
            "Sistema de Ecuaciones": ("sistema", MatrixSystemSolverWidget)
        }

        page_title = "Operaciones con {Matrices}"
        intro_text = (
            "👋 Bienvenido a la sección de operaciones con matrices.\n\n"
            "📌 Puedes realizar operaciones básicas con matrices, como: suma, resta, multiplicación.\n"
            "📌 Támbien puedes obtener el determinante, calcular inversas o resolver sistemas de ecuaciones lineales.\n"
        )

        intro_image_path = "assets/images/intro/matrix.png"

        super().__init__(manager, self.controller, operations, intro_text, intro_image_path, page_title)
    
    def execute_current_operation(self):
        label_key = next((label for label, (op_key, _) in self.operations.items() if op_key == self.current_operation), None)
        
        if not label_key:
            error_msg = f"No se encontró el widget para la operación: {self.current_operation}"
            self.show_message_dialog("Error", error_msg)
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
            self.show_message_dialog("🔴 ERROR", str(e))

        except Exception as e:
            self.show_message_dialog("🔴 ERROR", f"Error inesperado: {str(e)}")
            
    def show_result(self, result, message, operation_name=""):
        mostrar_matrices = ["Determinante", "Inversa", "Sistema de Ecuaciones"] # Implementar solución para determinante e inversa en el futuro :)

        if isinstance(result, list):
            if operation_name == "Determinante":
                for matrix_name, det_val in result:
                    result_matrix = Matrix(1, 1)
                    result_matrix.set_value(0, 0, det_val)
                    dialog = MatrixResultDialog([], result_matrix, operation=operation_name, parent=self)
                    dialog.exec()
                return

            if operation_name == "Inversa":
                for matrix_name, inverse_matrix in result:
                    if isinstance(inverse_matrix, Matrix):  # Si es una matriz, muestra la inversa
                        dialog = MatrixResultDialog([], inverse_matrix, operation=operation_name, parent=self)
                        dialog.exec()
                    else:  # Si es un error (string), muestra el mensaje
                        self.show_message_dialog("🔴 ERROR", inverse_matrix)
                return

        if isinstance(result, Matrix):
            if operation_name in mostrar_matrices:
                matrices = self.manager.get_all_matrices()
            else:
                matrices = []

            dialog = MatrixResultDialog(matrices, result, operation=operation_name, parent=self)
            dialog.exec()

    def _fill_result_table(self, matrix: Matrix):
        rows, cols = matrix.rows, matrix.cols
        self.result_table.setRowCount(rows)
        self.result_table.setColumnCount(cols)
        self.result_table.setHorizontalHeaderLabels([str(i + 1) for i in range(cols)])
        self.result_table.setVerticalHeaderLabels([str(i + 1) for i in range(rows)])

        # Configurar propiedades de selección
        self.result_table.setSelectionMode(QTableWidget.NoSelection)
        self.result_table.setFocusPolicy(Qt.NoFocus)

        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row in range(rows):
            for col in range(cols):
                value = matrix.data[row, col]
                item = QTableWidgetItem(f"{value:.2f}")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.result_table.setItem(row, col, item)
