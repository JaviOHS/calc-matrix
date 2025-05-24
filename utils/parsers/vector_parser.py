import re
from numpy import array
class VectorParser:
    VECTOR_PATTERN = re.compile(r'\[(-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?)*)\]') # Para op. [1] + [2]
    # VECTOR_PATTERN = re.compile(r'\[(-?\d+(?:\.\d+)?(?:,\s*-?\d+(?:\.\d+)?)+)\]') # Para op. [1,2] + [3,4]

    def parse_expression(self, expression: str):
        """Parsea la expresión de texto con operaciones entre vectores"""
        try:
            # Limpiar espacios innecesarios
            expression = self._clean_expression(expression)
            
            # Reemplazar el símbolo · por * antes de procesar
            expression = expression.replace('·', '*')
            
            matches = self.VECTOR_PATTERN.findall(expression)
            if not matches:
                raise ValueError("No se encontraron vectores válidos. Formato esperado: [n1,n2] + [n1,n2]")
            
            # Limpiar espacios en los números dentro de los vectores
            vectors = []
            for m in matches:
                # Limpiar espacios alrededor de las comas y convertir a array
                numbers = [float(x.strip()) for x in m.split(',')]
                vectors.append(array(numbers))

            dim = len(vectors[0])
            for v in vectors:
                if len(v) != dim:
                    raise ValueError("Todos los vectores deben tener la misma dimensión.")

            vector_map = {}
            for i, match in enumerate(matches):
                vector_map[f'v{i}'] = vectors[i]
                expression = expression.replace(f"[{match}]", f'v{i}', 1)

            return expression, vector_map
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise ValueError(f"Error al procesar la expresión: {str(e)}")

    def _clean_expression(self, expression: str) -> str:
        """Limpia espacios innecesarios de la expresión manteniendo la estructura"""
        # Eliminar espacios al inicio y final
        expression = expression.strip()
        
        # Eliminar espacios alrededor de operadores
        expression = re.sub(r'\s*([\+\-\*])\s*', r'\1', expression)
        
        # Eliminar espacios alrededor de corchetes
        expression = re.sub(r'\s*\[\s*', '[', expression)
        expression = re.sub(r'\s*\]\s*', ']', expression)
        
        return expression
