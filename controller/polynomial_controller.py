from utils.parsers.expression_parser import ExpressionParser

class PolynomialController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def execute_operation(self, operation_name: str, *args):
        if operation_name == "operaciones_combinadas":
            if len(args) != 1:
                raise ValueError("Se necesita una expresión para evaluar")
            return self.evaluate_combined_expression(args[0])
        elif operation_name == "raices":
            return self.get_roots()
        elif operation_name == "derivacion":
            return self.get_derivatives()
        elif operation_name == "integracion":
            if len(args) != 1:
                constant = 0  # Si no se pasa la constante, se establece a 0 por defecto
            else:
                constant = args[0]
            return self.get_integrals(constant)
        elif operation_name == "evaluacion":
            if len(args) != 1:
                raise ValueError("Se necesita un valor x para evaluar los polinomios")
            return self.evaluate_polynomials(args[0])
        else:
            raise ValueError(f"Operación no soportada: {operation_name}")

    def evaluate_combined_expression(self, expression):
        """Evalúa una expresión combinada de polinomios"""
        try:
            sym_expr = self.parser.parse_expression(expression)  # Parsear la expresión
            poly = self.parser.to_polynomial(sym_expr)  # Convertir la expresión a un polinomio (si es necesario)
            return poly
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión: {str(e)}")

    def divide_polynomials(self):
        try:
            result = self.manager.divide()
            return result
        except ValueError as e:
            raise ValueError(f"Error al dividir los polinomios: {e}")

    def evaluate_polynomials(self, x):
        try:
            results = self.manager.evaluate_all(x)
            return results
        except ValueError as e:
            raise ValueError(f"Error al evaluar los polinomios: {e}")

    def get_derivatives(self):
        try:
            results = self.manager.compute_derivatives()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular derivadas: {e}")

    def get_integrals(self, constant=0):
        try:
            results = self.manager.compute_integrals(constant)
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular integrales: {e}")

    def get_roots(self):
        try:
            results = []
            for idx, poly in enumerate(self.manager.polynomials):
                try:
                    roots = poly.get_roots()
                    results.append((f"P{idx+1}", roots))
                except ValueError as e:
                    results.append((f"P{idx+1}", str(e)))
            return results
        except Exception as e:
            raise ValueError(f"Error al calcular raíces: {e}")
