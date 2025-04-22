import numpy as np

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
        if self.data.shape != other.data.shape:
            raise ValueError("Las matrices deben tener el mismo tamaño.")
        return Matrix(self.rows, self.cols, self.data + other.data)

    def subtract(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Las matrices deben tener el mismo tamaño.")
        return Matrix(self.rows, self.cols, self.data - other.data)

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError("No se puede multiplicar: columnas de A ≠ filas de B.")
        result_data = np.dot(self.data, other.data)
        return Matrix(result_data.shape[0], result_data.shape[1], result_data)
    
    def divide(self, other):
        if self.rows != self.cols or other.rows != other.cols:
            raise ValueError("Ambas matrices deben ser cuadradas para la división.")
        if self.data.shape != other.data.shape:
            raise ValueError("Las matrices deben tener las mismas dimensiones.")
        det = np.linalg.det(other.data)
        if det == 0:
            raise ValueError("La matriz denominadora no es invertible (determinante = 0).")
        inverse_other = np.linalg.inv(other.data)
        result_data = np.dot(self.data, inverse_other)
        return Matrix(self.rows, self.cols, result_data)

    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada para calcular el determinante.")
        det = np.linalg.det(self.data)
        return round(det, 2)
    
    def inverse(self):
        if self.rows != self.cols:
            raise ValueError("La matriz debe ser cuadrada para calcular la inversa.")
        det = np.linalg.det(self.data)
        if det == 0:
            raise ValueError("La matriz no tiene inversa (determinante = 0).")
        inversa = np.linalg.inv(self.data)
        return Matrix(self.rows, self.cols, inversa)
    
    def solve(self, B):
        if self.rows != self.cols:
            raise ValueError("La matriz A debe ser cuadrada.")
        if self.rows != B.rows or B.cols != 1:
            raise ValueError("La matriz B debe tener las mismas filas que A y una sola columna.")
        det = np.linalg.det(self.data)
        if det == 0:
            raise ValueError("La matriz A no tiene inversa. No hay solución única.")
        solution = np.dot(np.linalg.inv(self.data), B.data)
        return Matrix(self.rows, 1, solution)
