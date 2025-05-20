from model.matrix_model import Matrix

class MatrixManager:
    def __init__(self):
        self.matrices = []

    def add_matrix(self, matrix: Matrix):
        if not isinstance(matrix, Matrix):
            raise TypeError("Se debe proporcionar una instancia de Matrix.")
        self.matrices.append(matrix)

    def clear(self):
        self.matrices.clear()

    def _ensure_matrices_exist(self, count=None):
        """Verifica que haya matrices suficientes"""
        if not self.matrices:
            raise ValueError('No hay matrices disponibles.')
        if count and len(self.matrices) < count:
            raise ValueError(f'Se necesitan al menos {count} matrices.')

    def sum_all(self):
        self._ensure_matrices_exist(2)
        result = self.matrices[0]
        for matrix in self.matrices[1:]:
            result = result.add(matrix)
        return result
    
    def subtract_all(self):
        self._ensure_matrices_exist(2)
        result = self.matrices[0]
        for matrix in self.matrices[1:]:
            result = result.subtract(matrix)
        return result
    
    def multiply_all(self):
        self._ensure_matrices_exist(2)
        result = self.matrices[0]
        for matrix in self.matrices[1:]:
            result = result.multiply(matrix)
        return result
    
    def divide_all(self):
        self._ensure_matrices_exist(2)
        matrix_1 = self.matrices[0]
        matrix_2 = self.matrices[1]
        return matrix_1.divide(matrix_2)

    def get_determinants(self):
        self._ensure_matrices_exist()
        resultados = []
        for idx, matrix in enumerate(self.matrices):
            det = matrix.determinant()
            resultados.append((f"M{idx+1}", det))
        return resultados

    def get_inverses(self):
        self._ensure_matrices_exist()
        resultados = []
        for idx, matrix in enumerate(self.matrices):
            inversa = matrix.inverse()
            resultados.append((f"M{idx+1}", inversa))
        return resultados
    
    def get_transpose(self):
        self._ensure_matrices_exist()
        resultados = []
        for idx, matrix in enumerate(self.matrices):
            transpuesta = matrix.transpose()
            resultados.append((f"M{idx+1}", transpuesta))
        return resultados

    def solve_system(self):
        self._ensure_matrices_exist(2)
        A = self.matrices[0]
        B = self.matrices[1]
        return A.solve(B)
    
    def get_all_matrices(self):
        self._ensure_matrices_exist()
        return self.matrices

    def get_vector_and_eigenvalues(self):
        self._ensure_matrices_exist()
        resultados = []
        for idx, matrix in enumerate(self.matrices):
            eigenvalues, eigenvectors = matrix.eigenvalues_and_eigenvectors()
            resultados.append((f"M{idx+1}", (eigenvalues, eigenvectors)))
        return resultados

    def validate_matrix_dimensions(self, matrix_a, matrix_b, operation):
        """Valida las dimensiones de las matrices según la operación"""
        if operation in ['add', 'subtract']:
            if matrix_a.data.shape != matrix_b.data.shape:
                raise ValueError("Las matrices deben tener el mismo tamaño.")
        elif operation == 'multiply':
            if matrix_a.cols != matrix_b.rows:
                raise ValueError("No se puede multiplicar: columnas de A ≠ filas de B.")
        elif operation == 'divide':
            if not all(m.rows == m.cols for m in [matrix_a, matrix_b]):
                raise ValueError("Ambas matrices deben ser cuadradas para la división.")
            if matrix_a.data.shape != matrix_b.data.shape:
                raise ValueError("Las matrices deben tener las mismas dimensiones.")

    def validate_single_matrix(self, matrix, operation):
        """Valida una única matriz para operaciones como determinante/inversa"""
        if operation in ['determinant', 'inverse', 'eigenvalues']:
            if matrix.rows != matrix.cols:
                raise ValueError(f"La matriz debe ser cuadrada para calcular {operation}.")
