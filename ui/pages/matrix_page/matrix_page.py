from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from model.matrix_model import Matrix
from ui.pages.base_page import BaseOperationPage
from ui.pages.matrix_page.operation_widgets.matrix_op import MatrixSimpleOP, MatrixDeterminant, MatrixInverse
from ui.pages.matrix_page.operation_widgets.solver_sys_widget import MatrixSystemSolverWidget
from ui.pages.matrix_page.operation_widgets.mult_widget import MatrixMultiplicationWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QMessageBox

class MatrixPage(BaseOperationPage):
    def __init__(self, manager: MatrixManager):
        self.controller = MatrixController(manager)

        operations = {
            "Suma": ("suma", MatrixSimpleOP),
            "Resta": ("resta", MatrixSimpleOP),
            "Multiplicación": ("multiplicacion", MatrixMultiplicationWidget),
            "División": ("division", MatrixSimpleOP),
            "Determinante": ("determinante", MatrixDeterminant),
            "Inversa": ("inversa", MatrixInverse),
            "Sistema de Ecuaciones": ("sistema", MatrixSystemSolverWidget)
        }

        intro_text = (
            "Bienvenido a la sección de operaciones con matrices.\n\n"
            "Puedes realizar suma, resta, multiplicación, obtener determinantes,\n"
            "inversas o resolver sistemas de ecuaciones lineales.\n"
        )

        intro_image_path = "assets/images/matrix_intro.png"
        page_title = "Operaciones con Matrices"

        super().__init__(manager, self.controller, operations, intro_text, intro_image_path, page_title)

    def execute_current_operation(self):
        operation_key = None
        for key, (op_name, _) in self.operations.items():
            if op_name == self.current_operation:
                operation_key = key
                break

        widget = self.operation_widgets.get(operation_key)
        if not widget:
            QMessageBox.critical(self, "Error", f"No se encontró el widget para la operación: {operation_key}")
            return

        try:
            matrices = widget.collect_matrices()
            self.manager.matrices.clear()
            for matrix in matrices:
                self.manager.add_matrix(matrix)

            result = self.controller.execute_operation(self.current_operation)
            self.show_result(result, f"{self.current_operation.capitalize()} realizada correctamente")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        self.result_label.setText(message)
        self.result_table.clear()

        if isinstance(result, list):
            if isinstance(result[0][1], Matrix):
                matrix = result[0][1]
                self._fill_result_table(matrix)
            else:
                text = "\n".join([f"{name}: {value}" for name, value in result])
                self.result_label.setText(f"{message}\n\n{text}")
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
        else:
            self._fill_result_table(result)

        self.stacked_widget.addWidget(self.result_widget)
        self.stacked_widget.setCurrentWidget(self.result_widget)

    def _fill_result_table(self, matrix: Matrix):
        rows, cols = matrix.rows, matrix.cols
        self.result_table.setRowCount(rows)
        self.result_table.setColumnCount(cols)
        self.result_table.setHorizontalHeaderLabels([str(i + 1) for i in range(cols)])
        self.result_table.setVerticalHeaderLabels([str(i + 1) for i in range(rows)])

        for row in range(rows):
            for col in range(cols):
                value = matrix.data[row, col]
                item = QTableWidgetItem(f"{value:.2f}")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.result_table.setItem(row, col, item)
