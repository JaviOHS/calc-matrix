from utils.parsers.expression_parser import ExpressionParser

class DistributionController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def execute_operation(self, operation, **kwargs):
        try:
            if operation == "generar_numeros":
                return self.generate_numbers(**kwargs)
            elif operation == "monte_carlo_integration":
                return self.monte_carlo_integration(**kwargs)
            else:
                raise ValueError(f"Operación no soportada: {operation}")
        except Exception as e:
            raise ValueError(f"Error en la operación: {str(e)}")

    def generate_numbers(self, algorithm="mersenne", count=5, seed=None, **kwargs):
        try:
            numbers = self.manager.generate_random_numbers(
                count=count,
                algorithm=algorithm,
                seed=seed,
                **kwargs  # Pasamos todos los parámetros adicionales
            )
            return {"success": True, "numbers": numbers, "count": len(numbers), "algorithm": algorithm}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def monte_carlo_integration(self, expression, a, b, n_points=10000, algorithm="mersenne", seed=None, **kwargs):
        """
        Realiza la integración numérica por Monte Carlo.
        
        Args:
            expression: Expresión a integrar (string)
            a: Límite inferior de integración
            b: Límite superior de integración
            n_points: Número de puntos aleatorios
            algorithm: Algoritmo de generación de números aleatorios
            seed: Semilla para el generador
            **kwargs: Argumentos adicionales para el generador
            
        Returns:
            dict: Resultado de la integración con información adicional
        """
        try:
            # Validar y preparar los parámetros
            if not expression:
                raise ValueError("La expresión no puede estar vacía.")
                
            try:
                a = float(a)
                b = float(b)
            except ValueError:
                raise ValueError("Los límites de integración deben ser números.")
                
            try:
                n_points = int(n_points)
                if n_points <= 0:
                    raise ValueError("El número de puntos debe ser positivo.")
            except ValueError:
                raise ValueError("El número de puntos debe ser un entero positivo.")
                
            # Parsear la expresión utilizando el parser existente
            parsed_expr = self.parser.parse_expression(expression)
            
            # Llamar al método del manager
            result = self.manager.calculate_monte_carlo_integration(parsed_expr, a, b, n_points, algorithm, seed, **kwargs)
            
            return {"success": True,**result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        
