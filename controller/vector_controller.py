from model.vector_model import Vector
import re
import numpy as np

class SympyVectorParser:
    VECTOR_PATTERN = re.compile(r'\[(-?\d+(?:\.\d+)?(?:,\s*-?\d+(?:\.\d+)?)+)\]')

    def parse_expression(self, expression: str):
        """Parsea la expresión de texto con operaciones entre vectores"""
        matches = self.VECTOR_PATTERN.findall(expression) # Extraer vectores
        if not matches:
            raise ValueError("No se encontraron vectores válidos.")
        
        vectors = [np.array([float(x) for x in m.split(',')]) for m in matches] # Convertir cada grupo a np.array

        dim = len(vectors[0])
        for v in vectors:
            if len(v) != dim:
                raise ValueError("Todos los vectores deben tener la misma dimensión.")

        vector_map = {} # Reemplazar los vectores por identificadores temporales v0, v1, ...
        for i, match in enumerate(matches):
            vector_map[f'v{i}'] = vectors[i]
            expression = expression.replace(f"[{match}]", f'v{i}', 1)

        return expression, vector_map

class VectorController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = SympyVectorParser()

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
            raise ValueError(f"Error al evaluar la operación: {e}")

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
            raise ValueError("El producto cruzado solo es válido para vectores en R3.")
        return np.cross(v1, v2)
    