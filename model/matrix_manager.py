from model.matrix_model import Matrix

class MatrixManager:
    def __init__(self):
        self.matrices = []

    def add_matrix(self, matrix: Matrix):
        if isinstance(matrix, list):
            raise TypeError("Se intentó agregar una lista de matrices en lugar de una matriz individual.")
        self.matrices.append(matrix)

    def clear(self):
        self.matrices.clear()

    def sum_all(self):
        if not self.matrices:
            raise ValueError('No hay matrices para sumar.')
        result = self.matrices[0]
        for matrix in self.matrices[1:]:
            result = result.add(matrix)
        return result
    
    def subtract_all(self):
        if not self.matrices:
            raise ValueError('No hay matrices para restar.')
        result = self.matrices[0]
        for matrix in self.matrices[1:]:
            result = result.subtract(matrix)
        return result
    
    def multiply_all(self):
        if len(self.matrices) < 2:
            raise ValueError("Se necesitan al menos dos matrices para multiplicar.")
        result = self.matrices[0]
        for matrix in self.matrices[1:]:
            result = result.multiply(matrix)
        return result
    
    def divide_all(self):
        if len(self.matrices) != 2:
            raise ValueError("Se necesitan exactamente dos matrices para dividir.")
        matrix_1 = self.matrices[0]
        matrix_2 = self.matrices[1]
        return matrix_1.divide(matrix_2)

    def get_determinants(self):
        if not self.matrices:
            raise ValueError("No hay matrices para calcular determinantes.")
        resultados = []
        for idx, matrix in enumerate(self.matrices):
            if not isinstance(matrix, Matrix):
                resultados.append((f"M{idx+1}", "Entrada inválida (no es una matriz)."))
                continue
            try:
                det = matrix.determinant()
                resultados.append((f"M{idx+1}", det))
            except ValueError as e:
                resultados.append((f"M{idx+1}", str(e)))
        return resultados

    def get_inverses(self):
        if not self.matrices:
            raise ValueError("No hay matrices para calcular inversas.")
        resultados = []
        for idx, matrix in enumerate(self.matrices):
            try:
                inversa = matrix.inverse()
                resultados.append((f"M{idx+1}", inversa))
            except ValueError as e:
                resultados.append((f"M{idx+1}", str(e)))
        return resultados

    def solve_system(self):
        if len(self.matrices) != 2:
            raise ValueError("Se necesitan exactamente dos matrices: A y B.")
        A = self.matrices[0]
        B = self.matrices[1]
        return A.solve(B)
    
    def get_all_matrices(self):
        if not self.matrices:
            raise ValueError("No hay matrices para mostrar.")
        return self.matrices
