class MatrixValidator:
    """Módulo para validaciones de matrices"""
    @staticmethod
    def validate_dimensions(matrix_a, matrix_b, operation):
        """Valida las dimensiones de matrices para determinada operación"""
        if operation in ['add', 'subtract']:
            if matrix_a.rows != matrix_b.rows or matrix_a.cols != matrix_b.cols:
                raise ValueError("Las matrices deben tener el mismo tamaño.")
        
        elif operation == 'multiply':
            if matrix_a.cols != matrix_b.rows:
                raise ValueError("No se puede multiplicar: columnas de A ≠ filas de B.")
        
        elif operation == 'divide':
            if matrix_a.rows != matrix_a.cols or matrix_b.rows != matrix_b.cols:
                raise ValueError("Ambas matrices deben ser cuadradas para la división.")
            if matrix_a.rows != matrix_b.rows:
                raise ValueError("Las matrices deben tener las mismas dimensiones.")
    
    @staticmethod
    def validate_square(matrix, operation_name):
        """Valida que una matriz sea cuadrada"""
        if matrix.rows != matrix.cols:
            raise ValueError(f"La matriz debe ser cuadrada para {operation_name}.")
    
    @staticmethod
    def validate_invertible(matrix):
        """Valida que una matriz sea invertible (det ≠ 0)"""
        from numpy import linalg
        det = linalg.det(matrix.data)
        if abs(det) < 1e-10:  # Usar un umbral pequeño para comparaciones de punto flotante
            raise ValueError("La matriz no es invertible (determinante = 0).")
    
    @staticmethod
    def validate_matrix_value(value, row=None, col=None, matrix_name=""):
        """Valida que un valor sea un número válido para una matriz"""
        from utils.validators.expression_validators import is_valid_number
        
        if not is_valid_number(value):
            position = f" en fila {row+1}, columna {col+1}" if row is not None and col is not None else ""
            prefix = f"{matrix_name}" if matrix_name else "Matriz"
            raise ValueError(f"{prefix}{position}: Valor inválido. Asegúrese de ingresar un número válido.")
        return float(value)
    
    @staticmethod
    def validate_table_values(table, matrix_name=""):
        """Valida todos los valores en una tabla QTableWidget"""
        values = []
        
        for r in range(table.rowCount()):
            row_values = []
            for c in range(table.columnCount()):
                item = table.item(r, c)
                value = item.text() if item else "0"
                # Validar y convertir a float
                valid_value = MatrixValidator.validate_matrix_value(value, r, c, matrix_name)
                row_values.append(valid_value)
            values.append(row_values)
            
        return values
