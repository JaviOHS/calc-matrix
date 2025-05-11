from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application,convert_xor,implicit_application,parse_expr
from model.polynomial_model import Polynomial
from utils.validators import exponents_validator
import sympy as sp
import re

class ExpressionParser:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Function('y')  # y(x) como función simbólica

        self.transformations = (
            standard_transformations +
            (implicit_multiplication_application, convert_xor, implicit_application)
        )

        self.allowed_symbols = {
            "x": self.x,
            "y": self.y,  # ya no es un símbolo, sino una función
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "ln": sp.ln,
            "log": sp.log,
            "sqrt": sp.sqrt,
            "e": sp.E,
            "pi": sp.pi,
            "Derivative": sp.Derivative,
            "Eq": sp.Eq,
            "diff": sp.Derivative,
            "exp": sp.exp,
            "Abs": sp.Abs,
            "π": sp.pi,
        }

        self.allowed_names = set(self.allowed_symbols.keys())

    def sanitize_expression(self, expr: str) -> str:
        # Reemplazos básicos
        replacements = {
            "−": "-", "×": "*", "÷": "/", "·": "*", "^": "**",
            "[": "(", "]": ")", "{": "(", "}": ")", "sen": "sin",
            "=": "=="
        }
        for bad, good in replacements.items():
            expr = expr.replace(bad, good)

        # Notación de derivadas comunes (orden importa: primero las segundas derivadas)
        expr = re.sub(r"d\^?2y/dx\^?2", "Derivative(y(x), (x, 2))", expr)  # incluye d2y/dx2 y d^2y/dx^2
        expr = re.sub(r"d²y/dx²", "Derivative(y(x), (x, 2))", expr)  # soporta notación unicode
        expr = re.sub(r"dy/dx", "Derivative(y(x), x)", expr)

        # También soportar notaciones con comillas simples, si no tienen paréntesis
        expr = re.sub(r"y''(?!\()", "Derivative(y(x), (x, 2))", expr)
        expr = re.sub(r"y'(?!\()", "Derivative(y(x), x)", expr)

        # Reemplazar 'y' por 'y(x)' solo cuando no es parte de 'y(x)', 'y''', etc.
        expr = re.sub(r'\by\b(?!\s*\()', "y(x)", expr)

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
       
    def parse_equation(self, raw_expr: str):
        try:
            clean_expr = self.sanitize_expression(raw_expr)
            
            # Manejar el caso especial donde ya viene como Eq
            if clean_expr.startswith("Eq("):
                return parse_expr(clean_expr, local_dict=self.allowed_symbols)
            
            # Dividir en LHS y RHS
            if '==' in clean_expr:
                lhs, rhs = clean_expr.split('==', 1)
                lhs_expr = parse_expr(lhs.strip(), transformations=self.transformations, 
                                    local_dict=self.allowed_symbols)
                rhs_expr = parse_expr(rhs.strip(), transformations=self.transformations, 
                                    local_dict=self.allowed_symbols)
                return sp.Eq(lhs_expr, rhs_expr)
            else:
                # Si no hay igual, asumir == 0
                expr = parse_expr(clean_expr, transformations=self.transformations, 
                                local_dict=self.allowed_symbols)
                return sp.Eq(expr, 0)
        except Exception as e:
            raise ValueError(f"Error al analizar la ecuación: {e}")
            