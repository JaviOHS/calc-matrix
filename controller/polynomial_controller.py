from utils.parsers.expression_parser import ExpressionParser


class PolynomialController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def execute_operation(self, operation_name: str, *args):
        if operation_name == "combined_operations":
            if len(args) != 1:
                raise ValueError("Se necesita una expresión para evaluar.")
            return self.evaluate_combined_expression(args[0])
        elif operation_name == "roots":
            return self.get_roots()
        elif operation_name == "derivative":
            return self.get_derivatives()
        elif operation_name == "integral":
            if len(args) != 1:
                constant = 0  # Si no se pasa la constante, se establece a 0 por defecto
            else:
                constant = args[0]
            return self.get_integrals(constant)
        elif operation_name == "evaluation":
            if len(args) != 1:
                raise ValueError("Se necesita un valor x para evaluar los polinomios.")
            return self.evaluate_polynomials(args[0])
        else:
            raise ValueError(f"Operación no soportada: {operation_name}")

    def evaluate_combined_expression(self, expression):
        """Evalúa una expresión combinada de polinomios"""
        try:
            sym_expr = self.parser.parse_expression(expression)  # Parsear la expresión
            if sym_expr.is_polynomial():
                poly = self.parser.to_polynomial(sym_expr)  # Convertir la expresión a un polinomio (si es necesario)
                return poly
            else:
                raise ValueError("La expresión no es un polinomio válido.")
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión:\n{str(e)}")

    def evaluate_polynomials(self, x):
        try:
            results = self.manager.evaluate_all(x)
            return results
        except ValueError as e:
            raise ValueError(f"Error al evaluar los polinomios:\n{e}")

    def get_derivatives(self):
        try:
            results = []
            derivatives = self.manager.compute_derivatives()
            for idx, derivative in enumerate(derivatives):
                results.append((f"P{idx+1}", derivative))
            return results[0][1]  # Devuelve solo el resultado sin el P1
        except ValueError as e:
            raise ValueError(f"Error al calcular derivadas:\n{e}")

    def get_integrals(self, constant=0):
        try:
            results = []
            integrals = self.manager.compute_integrals(constant)
            for idx, integral in enumerate(integrals):
                results.append((f"P{idx+1}", integral))
            return results[0][1]  # Devuelve solo el resultado sin el P1
        except ValueError as e:
            raise ValueError(f"Error al calcular integrales:\n{e}")

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
            raise ValueError(f"Error al calcular raíces:\n{e}")
