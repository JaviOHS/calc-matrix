from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application,convert_xor,implicit_application,parse_expr
from model.polynomial_model import Polynomial
from utils.validators import exponents_validator
import sympy as sp
import re

class ExpressionParser:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Function('y')  # y(x) como función simbólica para 2D
        self.y_symbol = sp.Symbol('y')  # y como variable independiente para 3D

        self.transformations = (
            standard_transformations +
            (implicit_multiplication_application, convert_xor, implicit_application)
        )

        # Diccionario base con símbolos comunes
        self.common_symbols = {
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
        
        # Símbolos para expresiones 2D (y es una función)
        self.allowed_symbols_2d = self.common_symbols.copy()
        self.allowed_symbols_2d.update({
            "x": self.x,
            "y": self.y,  # y como función y(x)
        })

        # Símbolos para expresiones 3D (y es una variable independiente)
        self.allowed_symbols_3d = self.common_symbols.copy()
        self.allowed_symbols_3d.update({
            "x": self.x,
            "y": self.y_symbol,  # y como variable independiente
        })

        self.allowed_names = set(self.common_symbols.keys()) | {"x", "y"}

    def sanitize_expression(self, expr: str, use_3d=False) -> str:
        # Reemplazos básicos
        replacements = {
            "−": "-", "×": "*", "÷": "/", "·": "*", "^": "**",
            "[": "(", "]": ")", "{": "(", "}": ")", "sen": "sin",
            "=": "=="
        }
        for bad, good in replacements.items():
            expr = expr.replace(bad, good)

        # Solo aplicar reemplazos específicos de EDO si no estamos en modo 3D
        if not use_3d:
            # Notación de derivadas comunes (orden importa: primero las segundas derivadas)
            expr = re.sub(r"d\^?2y/dx\^?2", "Derivative(y(x), (x, 2))", expr)
            expr = re.sub(r"d²y/dx²", "Derivative(y(x), (x, 2))", expr)
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

    def parse_expression(self, raw_expr: str, use_3d=False, max_length: int = 500):
        """
        Analiza una expresión matemática y la convierte a formato sympy
        
        Args:
            raw_expr (str): Expresión matemática a parsear
            use_3d (bool): Si es True, interpreta x,y como variables independientes para gráficas 3D
            max_length (int): Longitud máxima permitida para la expresión
            
        Returns:
            sympy.Expr: Expresión parseada en formato sympy
        """
        try:
            if len(raw_expr) > max_length:
                raise ValueError(f"La expresión es demasiado larga (máximo permitido: {max_length} caracteres).")

            if not exponents_validator(raw_expr):
                raise ValueError("El exponente ingresado es demasiado alto. Por favor, utilice exponentes menores a 1000 para evitar bloqueos.")
            
            # Determinar qué conjunto de símbolos usar según el modo
            allowed_symbols = self.allowed_symbols_3d if use_3d else self.allowed_symbols_2d
            
            # Sanitizar la expresión considerando el modo
            clean_expr = self.sanitize_expression(raw_expr, use_3d)
            self.validate_symbols(clean_expr)
            
            # Parsear usando los símbolos apropiados para el modo
            parsed = parse_expr(clean_expr, transformations=self.transformations, local_dict=allowed_symbols)
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
                return parse_expr(clean_expr, local_dict=self.allowed_symbols_2d)
            
            # Dividir en LHS y RHS
            if '==' in clean_expr:
                lhs, rhs = clean_expr.split('==', 1)
                lhs_expr = parse_expr(lhs.strip(), transformations=self.transformations, local_dict=self.allowed_symbols_2d)
                rhs_expr = parse_expr(rhs.strip(), transformations=self.transformations, local_dict=self.allowed_symbols_2d)
                return sp.Eq(lhs_expr, rhs_expr)
            else:
                # Si no hay igual, asumir == 0
                expr = parse_expr(clean_expr, transformations=self.transformations, local_dict=self.allowed_symbols_2d)
                return sp.Eq(expr, 0)
        except Exception as e:
            raise ValueError(f"Error al analizar la ecuación: {e}")
