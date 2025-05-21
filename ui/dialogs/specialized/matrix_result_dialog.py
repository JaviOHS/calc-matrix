from ui.dialogs.base.base_result_dialog import BaseResultDialog
from PySide6.QtCore import Qt

class MatrixResultDialog(BaseResultDialog):
    def __init__(self, result_matrix, operation="", parent=None):
        super().__init__(operation, parent)
        
        # Verificar que sea una matriz válida
        if hasattr(result_matrix, 'rows') and hasattr(result_matrix, 'cols'):
            # Crear y añadir tabla de matriz
            matrix_widget, _ = self.create_data_table(
                rows=result_matrix.rows, 
                cols=result_matrix.cols,
                data_accessor=lambda r, c: result_matrix.data[r, c],
                needs_scroll=result_matrix.rows > 5
            )
            self.result_layout.addWidget(matrix_widget, 0, Qt.AlignCenter)
        
        # Finalizar configuración
        self.finalize()

class EigenvectorsDialog(BaseResultDialog):
    def __init__(self, eigenvalues, eigenvectors, operation="", parent=None):
        super().__init__(operation, parent)
        
        # Tabla de valores propios
        eigenvalues_widget, _ = self.create_data_table(
            rows=1, 
            cols=len(eigenvalues),
            data_accessor=lambda r, c: eigenvalues[c]
        )
        self.add_section("📌 VALORES PROPIOS", eigenvalues_widget)
        
        # Tabla de vectores propios
        eigenvectors_widget, _ = self.create_data_table(
            rows=eigenvectors.shape[0], 
            cols=eigenvectors.shape[1],
            data_accessor=lambda r, c: eigenvectors[r, c],
            needs_scroll=eigenvectors.shape[0] > 6
        )
        self.add_section("📌 VECTORES PROPIOS", eigenvectors_widget)
        
        # Finalizar configuración
        self.finalize()
        