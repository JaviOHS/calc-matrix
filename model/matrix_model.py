import numpy as np
from utils.validators.matrix_validator import MatrixValidator

class Matrix:
    def __init__(self, rows, cols=None, data=None):
        if cols is None:
            cols = rows
        self.rows = rows
        self.cols = cols
        if data is not None:
            self.data = np.array(data)
        else:
            self.data = np.zeros((rows, cols))

    def set_value(self, row, col, value):
        self.data[row, col] = float(value)

    def __repr__(self):
        return str(self.data)

    def add(self, other):
        MatrixValidator.validate_dimensions(self, other, 'add')
        return Matrix(self.rows, self.cols, self.data + other.data)

    def subtract(self, other):
        MatrixValidator.validate_dimensions(self, other, 'subtract')
        return Matrix(self.rows, self.cols, self.data - other.data)

    def multiply(self, other):
        MatrixValidator.validate_dimensions(self, other, 'multiply')
        result_data = np.dot(self.data, other.data)
        return Matrix(self.rows, other.cols, result_data)
    
    def divide(self, other):
        MatrixValidator.validate_dimensions(self, other, 'divide')
        MatrixValidator.validate_invertible(other)
        inverse_other = np.linalg.inv(other.data)
        result_data = np.dot(self.data, inverse_other)
        return Matrix(self.rows, self.cols, result_data)

    def determinant(self):
        MatrixValidator.validate_square(self, "calcular el determinante")
        return round(np.linalg.det(self.data), 12)
    
    def inverse(self):
        MatrixValidator.validate_square(self, "calcular la inversa")
        MatrixValidator.validate_invertible(self)
        inversa = np.linalg.inv(self.data)
        return Matrix(self.rows, self.cols, inversa)
    
    def solve(self, B):
        MatrixValidator.validate_square(self, "resolver el sistema")
        MatrixValidator.validate_dimensions(self, B, 'solve')
        MatrixValidator.validate_invertible(self)
        solution = np.dot(np.linalg.inv(self.data), B.data)
        return Matrix(self.rows, 1, solution)
    
    def transpose(self):
        """Calcula la transpuesta de la matriz."""
        return Matrix(self.cols, self.rows, self.data.T)

    def eigenvalues_and_eigenvectors(self):
        """Calcula los valores y vectores propios de la matriz."""
        MatrixValidator.validate_square(self, "calcular los valores y vectores propios")
        eigenvalues, eigenvectors = np.linalg.eig(self.data)
        return eigenvalues, eigenvectors