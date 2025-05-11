import numpy as np
from utils.parsers.vector_parser import VectorParser

class VectorController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = VectorParser()

    def execute_operation(self, operation, expression):
        if operation == "magnitud":
            return self.calculate_magnitude(expression)
        elif operation == "producto_punto":
            return self.dot_product(expression)
        elif operation == "producto_cruzado":
            return self.cross_product(expression)
        else:
            return self.evaluate_basic_expression(expression)

    def evaluate_basic_expression(self, expression):
        expr, vector_map = self.parser.parse_expression(expression)
        
        try:
            result = eval(expr, {}, vector_map)
            return result
        except Exception as e:
            raise ValueError(f"Error al evaluar la operación: Ingrese vectores válidos.")

    def calculate_magnitude(self, expression):
        expr, vector_map = self.parser.parse_expression(expression)
        if len(vector_map) != 1:
            raise ValueError("Solo se requiere un vector para calcular magnitud.")
        vector = list(vector_map.values())[0]
        return np.linalg.norm(vector)

    def dot_product(self, expression):
        expr, vector_map = self.parser.parse_expression(expression)
        if len(vector_map) != 2:
            raise ValueError("Se requieren exactamente dos vectores para producto punto.")
        v1, v2 = vector_map.values()
        return np.dot(v1, v2)

    def cross_product(self, expression):
        expr, vector_map = self.parser.parse_expression(expression)
        if len(vector_map) != 2:
            raise ValueError("Se requieren exactamente dos vectores para producto cruzado.")
        v1, v2 = vector_map.values()
        if len(v1) != 3 or len(v2) != 3:
            raise ValueError("El producto cruzado solo es válido para vectores de 3 dimensiones.")
        return np.cross(v1, v2)
    