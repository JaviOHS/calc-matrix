from model.matrix_manager import MatrixManager
from controller.matrix_controller import MatrixController
from model.matrix_model import Matrix
from ui.pages.base_page import BaseOperationPage
from ui.pages.matrix_page.operation_widgets.matrix_op import MatrixSimpleOP, MatrixDeterminant, MatrixInverse
from ui.pages.matrix_page.operation_widgets.solver_sys_widget import MatrixSystemSolverWidget
from ui.pages.matrix_page.operation_widgets.mult_widget import MatrixMultiplicationWidget
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from ui.pages.dialogs.matrix_result_dialog import MatrixResultDialog

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

    def prepare_operation(self, operation_key):
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        super().prepare_operation(operation_key)
        self.title_label.setText(f"{self.page_title} - {operation_key}")
    
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
            self.show_result(result, f"{self.current_operation.capitalize()} realizada correctamente", operation_key)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def show_result(self, result, message, operation_name=""):
        # Operaciones que requieren mostrar también las matrices originales
        mostrar_matrices = ["Determinante", "Inversa", "Sistema de Ecuaciones"]

        if isinstance(result, list):  # Si el resultado es una lista (como para inversas o determinantes)
            if operation_name == "Determinante":
                # Para determinante, mostramos el resultado usando un dialog de MatrixResultDialog
                # El result es una lista con el nombre de la matriz y su determinante
                matrix_name, determinant_value = result[0]  # Suponiendo que result es [('M1', det_value)]
                result_matrix = Matrix(1, 1)  # Creamos una "matriz" ficticia de 1x1 solo para mostrar el valor
                result_matrix.set_value(0, 0, determinant_value)  # Asignamos el determinante en la "matriz"

                dialog = MatrixResultDialog([], result_matrix, operation=operation_name, parent=self)
                dialog.exec()
                return

            elif operation_name == "Inversa":
                # Para inversas, mostramos la matriz inversa
                matrix_name, inverse_matrix = result[0]  # Suponiendo que result es [('M1', inverse_matrix)]
                dialog = MatrixResultDialog([], inverse_matrix, operation=operation_name, parent=self)
                dialog.exec()
                return

        if isinstance(result, Matrix):
            if operation_name in mostrar_matrices:
                matrices = self.manager.get_all_matrices()
            else:
                matrices = []

            dialog = MatrixResultDialog(matrices, result, operation=operation_name, parent=self)
            dialog.exec()
        else:
            # Para resultados no-matriz (escalares, como determinante simple)
            QMessageBox.information(self, "Resultado", str(result))

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
