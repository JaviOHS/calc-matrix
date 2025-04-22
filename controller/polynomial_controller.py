from model.polynomial_model import Polynomial
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor, implicit_application
import sympy as sp
import re
from utils.validators import validar_exponentes

class SympyPolynomialParser:
    def __init__(self):
        self.x = sp.Symbol('x')  # Usar 'x' como símbolo
        self.transformations = (
            standard_transformations +
            (implicit_multiplication_application, convert_xor, implicit_application)
        )

    def sanitize_expression(self, expression: str) -> str:
        replacements = {
            "−": "-",  # signo menos Unicode
            "×": "*",  # signo de multiplicación
            "÷": "/",  # signo de división
            "·": "*",  # punto medio
            "^": "**", # caret
            "[": "(", "]": ")",
            "{": "(", "}": ")",
        }
        for bad, good in replacements.items():
            expression = expression.replace(bad, good)

        # Insertar multiplicación implícita: 2( → 2*(
        expression = re.sub(r'(?<=\d)(\s*\()', r'*(', expression)

        # Corregir divisiones ambiguas tipo: /2(x+1) o /x(x+1)
        expression = re.sub(
            r'/\s*([a-zA-Z0-9.]+)\s*\(',  # algo como /2( o /x(
            lambda m: f'/({m.group(1)}*(', expression
        )

        # Cerrar paréntesis abiertos automáticamente si hicimos /(x*(...
        open_count = expression.count('(')
        close_count = expression.count(')')
        if close_count < open_count:
            expression += ')' * (open_count - close_count)

        return expression

    def parse_expression(self, expression: str):
        """Convierte una expresión en una estructura evaluable por sympy"""
        try:
            if not validar_exponentes(expression):
                raise ValueError("El exponente ingresado es demasiado alto. Por favor, utilice exponentes menores a 1000 para evitar bloqueos.")

            clean_expr = self.sanitize_expression(expression)
            parsed_expr = parse_expr(clean_expr, transformations=self.transformations, local_dict={"x": self.x})
            simplified_expr = sp.expand(parsed_expr)
            return simplified_expr
        except ValueError as ve:
            # Propagar errores personalizados
            raise ve
        except Exception as e:
            # Solo capturar errores generales
            raise ValueError("Error al parsear la expresión: Asegúrese de que la expresión sea válida.")

    def to_polynomial(self, sympy_expr):
        try:
            poly_expr = sp.Poly(sympy_expr, self.x, domain='QQ')  # QQ fuerza coeficientes racionales
            coeffs = poly_expr.all_coeffs()
            return Polynomial([sp.Rational(c) for c in coeffs])
        except Exception:
            raise ValueError(
                "La expresión no representa un polinomio válido. "
                "Asegúrese de que la expresión contenga sólo potencias enteras de x con coeficientes numéricos. "
                "Ejemplos válidos: 'x^2 + 2x + 1'. Ejemplos inválidos: 'sin(x)', '1/x', 'x^a', 'log(x)'."
            )
    
class PolynomialController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = SympyPolynomialParser()

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
        