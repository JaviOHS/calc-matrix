from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application,convert_xor,implicit_application,parse_expr
from model.polynomial_model import Polynomial
from utils.validators import exponents_validator
import sympy as sp
import re

class ExpressionParser:
    def __init__(self):
        self.x, self.y = sp.symbols('x y')
        self.transformations = (
            standard_transformations +
            (implicit_multiplication_application, convert_xor, implicit_application)
        )
        self.allowed_symbols = {
            "x": self.x,
            "y": self.y,
            "sen": sp.sin,  # Para soporte en español
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "ln": sp.ln,
            "log": sp.log,
            "sqrt": sp.sqrt,
            "e": sp.E,
            "pi": sp.pi
        }
        self.allowed_names = set(self.allowed_symbols.keys())

    def sanitize_expression(self, expr: str) -> str:
        replacements = {
            "−": "-", "×": "*", "÷": "/", "·": "*", "^": "**",
            "[": "(", "]": ")", "{": "(", "}": ")", "sen": "sin"
        }
        for bad, good in replacements.items():
            expr = expr.replace(bad, good)

        expr = re.sub(r'(?<=\d)(\s*\()', r'*(', expr)
        expr = re.sub(r'(?<=\d)(\s*[a-zA-Z])', r'*\1', expr)
        expr = re.sub(r'(?<=\))(\s*[a-zA-Z0-9])', r'*\1', expr)

        open_count = expr.count('(')
        close_count = expr.count(')')
        if close_count < open_count:
            expr += ')' * (open_count - close_count)

        return expr

    def validate_symbols(self, expr: str):
        pattern = r'\b([a-zA-Z][a-zA-Z0-9]*)\b'
        found_symbols = set(re.findall(pattern, expr))
        invalid_symbols = found_symbols - self.allowed_names
        if invalid_symbols:
            raise ValueError(
                f"Símbolos no permitidos encontrados: {', '.join(invalid_symbols)}\n"
                f"Símbolos permitidos: {', '.join(sorted(self.allowed_names))}"
            )

    def parse_expression(self, raw_expr: str, max_length: int = 500):
        try:
            if len(raw_expr) > max_length:
                raise ValueError(f"La expresión es demasiado larga (máximo permitido: {max_length} caracteres).")

            if not exponents_validator(raw_expr):
                raise ValueError("El exponente ingresado es demasiado alto. Por favor, utilice exponentes menores a 1000 para evitar bloqueos.")
            
            clean_expr = self.sanitize_expression(raw_expr)
            self.validate_symbols(clean_expr)
            parsed = parse_expr(clean_expr, transformations=self.transformations, local_dict=self.allowed_symbols)
            return sp.expand(parsed)
        except ValueError as e:
            raise ValueError(f"{str(e)}")
        except Exception as e:
            raise ValueError(f"Error al procesar la expresión: {str(e)}")

    def to_polynomial(self, sympy_expr):
        try:
            poly_expr = sp.Poly(sympy_expr, self.x, domain='QQ')
            coeffs = poly_expr.all_coeffs()
            return Polynomial([sp.Rational(c) for c in coeffs])
        except ValueError:
            raise ValueError(
                "La expresión no representa un polinomio válido. Asegúrese de que la expresión contenga sólo potencias enteras de x con coeficientes numéricos."
            )
        except Exception:
            raise ValueError(
                "Hubo un error al intentar convertir la expresión en un polinomio. Verifique la expresión."
            )

        