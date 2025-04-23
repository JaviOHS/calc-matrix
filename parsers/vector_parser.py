import re
import numpy as np

class VectorParser:
    VECTOR_PATTERN = re.compile(r'\[(-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?)*)\]') # Para op. [1] + [2]
    # VECTOR_PATTERN = re.compile(r'\[(-?\d+(?:\.\d+)?(?:,\s*-?\d+(?:\.\d+)?)+)\]') # Para op. [1,2] + [3,4]

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
