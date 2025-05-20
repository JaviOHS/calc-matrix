from model.matrix_model import Matrix
from ui.dialogs.specialized.matrix_result_dialog import MatrixResultDialog, EigenvectorsDialog

class ResultHandler:
    @staticmethod
    def show_matrix_result(result, operation_name, parent=None):
        """Muestra resultados de operaciones matriciales en diálogos apropiados"""
        if isinstance(result, Matrix):
            dialog = MatrixResultDialog(result, operation=operation_name, parent=parent)
            dialog.exec()
            return True

        if isinstance(result, list):
            dialog_map = {
                "Inversa": MatrixResultDialog,
                "Transpuesta": MatrixResultDialog,
            }

            if operation_name == "Determinante":
                for matrix_name, det_val in result:
                    if isinstance(det_val, (int, float)):
                        result_matrix = Matrix(1, 1)
                        result_matrix.set_value(0, 0, det_val)
                        dialog = MatrixResultDialog(result_matrix, operation=operation_name, parent=parent)
                        dialog.exec()
                return True

            if operation_name in dialog_map:
                dialog_type = dialog_map[operation_name]
                for matrix_name, matrix_result in result:
                    if isinstance(matrix_result, Matrix):
                        dialog = dialog_type(matrix_result, operation=operation_name, parent=parent)
                        dialog.exec()
                return True

            if operation_name == "Vectores y Valores Propios":
                for matrix_name, (eigenvalues, eigenvectors) in result:
                    dialog = EigenvectorsDialog(eigenvalues, eigenvectors, operation=operation_name, parent=parent)
                    dialog.exec()
                return True

        return False