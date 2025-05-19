from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application,convert_xor,implicit_application,parse_expr
from model.polynomial_model import Polynomial
from utils.validators.expression_validators import exponents_validator, validate_characters, validate_parentheses,validate_symbols,validate_expression_syntax
from utils.patterns import MATH_SYMBOLS, ODE_PATTERNS, SPECIAL_CHARS, ALLOWED_CHARS, ALLOWED_DIFFERENTIAL_CHARS
import sympy as sp
import re
import numpy as np
import functools

def expression_error_handler(func):
    """Decorador para manejar errores comunes en el procesamiento de expresiones matemáticas."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            error_msg = str(e).lower()
            if "name 'y' is not defined" in error_msg:
                raise ValueError("La variable 'y' solo está permitida en gráficas 3D y ecuaciones diferenciales.")
            elif "invalid syntax" in error_msg:
                raise ValueError("Sintaxis inválida en la expresión.")
            elif "overflow" in error_msg or "out of range" in error_msg:
                raise ValueError("Resultado numérico fuera de rango durante la evaluación.")
            else:
                raise ValueError(f"Error al procesar la expresión: {str(e)}")
    
    return wrapper

class ExpressionParser:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Function('y')  # y(x) como función simbólica para 2D
        self.y_symbol = sp.Symbol('y')  # y como variable independiente para 3D

        self.transformations = (standard_transformations +(implicit_multiplication_application, convert_xor, implicit_application))

        # Diccionario base con símbolos comunes
        self.common_symbols = {
            "sin": sp.sin,
            "sen": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "ln": sp.ln,
            "log": sp.log,
            "sqrt": sp.sqrt,
            "exp": sp.exp,
            "Abs": sp.Abs,
            "e": sp.E,
            "pi": sp.pi,
            "π": sp.pi,
            "Derivative": sp.Derivative,
            "diff": sp.Derivative,
            "Eq": sp.Eq,
        }
        
        self.allowed_symbols_2d = self.common_symbols.copy() # Símbolos para expresiones 2D (y es una función)
        self.allowed_symbols_2d.update({"x": self.x, "y": self.y}) # y como función y(x)

        self.allowed_symbols_3d = self.common_symbols.copy() # Símbolos para expresiones 3D (y es una variable independiente)
        self.allowed_symbols_3d.update({"x": self.x, "y": self.y_symbol}) # y como variable independiente

        # Nombres permitidos para la validación de símbolos
        self.allowed_names = set(self.common_symbols.keys()) | {"x", "y", "dx", "dy"}

        self.allowed_chars = ALLOWED_CHARS # Usar ambos conjuntos de caracteres
        self.allowed_differential_chars = ALLOWED_DIFFERENTIAL_CHARS
        self.special_chars_map = SPECIAL_CHARS

    def sanitize_expression(self, expr: str, use_3d=False) -> str:
        """ Sanitiza la expresión matemática para evitar errores de sintaxis."""
        for bad, good in MATH_SYMBOLS.items():
            expr = expr.replace(bad, good) # Aplicar reemplazos básicos

        if not use_3d:
            for pattern, replacement in ODE_PATTERNS.items():
                expr = re.sub(pattern, replacement, expr) # Solo aplicar reemplazos específicos de EDO si no estamos en modo 3D
                
        return expr

    def validate_expression(self, expr: str, max_length: int, allowed_chars: set, is_differential: bool = False, use_3d: bool = False):
        """Realiza todas las validaciones comunes para una expresión matemática."""
        if not expr.strip():
            raise ValueError("La expresión está vacía.")

        if len(expr) > max_length:
            raise ValueError(f"La expresión es demasiado larga (máximo: {max_length} caracteres).")

        is_valid, error_msg = exponents_validator(expr) # Validar exponentes
        if not is_valid:
            raise ValueError(error_msg)
        
        is_valid, error_msg = validate_expression_syntax(expr) # Validar sintaxis
        if not is_valid:
            raise ValueError(error_msg)
        
        is_valid, error_msg = validate_parentheses(expr) # Validar paréntesis
        if not is_valid:
            raise ValueError(error_msg)

        is_valid, error_msg = validate_characters(expr, allowed_chars, self.special_chars_map) # Validar caracteres
        if not is_valid:
            raise ValueError(error_msg)

        is_valid, error_msg = validate_symbols(expr, self.allowed_names, use_3d or is_differential, is_differential) # Validar símbolos
        if not is_valid:
            raise ValueError(error_msg)

    @expression_error_handler
    def parse_expression(self, raw_expr: str, use_3d=False, max_length: int = 500, is_differential=False):
        """Analiza una expresión matemática (POLINOMIOS) y la convierte a formato sympy."""
        allowed_chars = self.allowed_differential_chars if is_differential else self.allowed_chars
        self.validate_expression(raw_expr, max_length, allowed_chars, is_differential, use_3d)

        clean_expr = self.sanitize_expression(raw_expr, use_3d) # Sanitizar la expresión
        allowed_symbols = self.allowed_symbols_3d if (use_3d or is_differential) else self.allowed_symbols_2d # Definir el diccionario de símbolos permitidos
        parsed = parse_expr(clean_expr, transformations=self.transformations, local_dict=allowed_symbols) # Convertir a expresión sympy

        if parsed.is_constant():
            return float(parsed.evalf()) # Si es una constante, devolverla como float

        return sp.expand(parsed)

    @expression_error_handler
    def to_polynomial(self, sympy_expr):
        """Convierte una expresión sympy a un objeto Polynomial."""
        poly_expr = sp.Poly(sympy_expr, self.x, domain='QQ')
        coeffs = poly_expr.all_coeffs()
        return Polynomial([sp.Rational(c) for c in coeffs])
       
    @expression_error_handler
    def parse_equation(self, raw_expr: str):
        """Parsea una ecuación (EDOs) y la convierte en una expresión sympy Eq."""
        self.validate_expression(raw_expr, max_length=500, allowed_chars=self.allowed_differential_chars, is_differential=True, use_3d=False)
        clean_expr = self.sanitize_expression(raw_expr)

        if clean_expr.startswith("Eq("):
            return parse_expr(clean_expr, local_dict=self.allowed_symbols_2d) # Manejar el caso especial donde ya viene como Eq

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
        
    @expression_error_handler
    def parse_ode_for_numerical(self, raw_expr: str):
        """Parsea una ecuación diferencial de la forma dy/dx = f(x, y) y devuelve una función lambda f(x, y) para métodos numéricos."""
        raw_expr = raw_expr.strip() # Eliminar espacios innecesarios y asegurarse de que hay RHS
        if raw_expr.endswith('='):
            raw_expr += '0'

        preprocessed_expr = self._preprocess_ode_expression(raw_expr) # Normalizar la ecuación sin convertirla a Derivative
        rhs_expr = self._extract_rhs_from_equation(preprocessed_expr) # Extraer el RHS
        rhs_clean = self.sanitize_expression(rhs_expr, use_3d=True) # Sanitizar solo el RHS (evita errores con y(x) en modo 3D)
        parsed_expr = self.parse_expression(rhs_clean, use_3d=True, is_differential=True) # Parsear solo el RHS como función de x e y

        # Crear función lambda evaluable f(x, y) con manejo de errores
        def safe_lambdify(x, y):
            try:
                result = sp.lambdify([self.x, self.y_symbol], parsed_expr, modules=['numpy'])(x, y)
                if not np.isfinite(result):
                    raise OverflowError("Resultado numérico fuera de rango.")
                return result
            except OverflowError:
                raise ValueError("Resultado numérico fuera de rango durante la evaluación de la ecuación diferencial.")
            
        return safe_lambdify, rhs_clean

    def _preprocess_ode_expression(self, expr: str):
        """Normaliza la ecuación sin convertirla a Derivative, para evitar errores al parsear en modo 3D."""
        expr = re.sub(r'd\s*y\s*/\s*d\s*x', 'dy/dx', expr)
        expr = re.sub(r'Δ', 'd', expr)  # En caso de copiar y pegar símbolos raros
        return expr

    def _extract_rhs_from_equation(self, equation: str) -> str:
        """ Extrae el lado derecho (RHS) de una ecuación del tipo dy/dx = ... Si no hay '=', se asume que la entrada ya es el RHS."""
        equation = equation.strip()

        if '=' in equation:
            lhs, rhs = equation.split('=', 1)
            rhs = rhs.strip()
            return rhs or '0'
        else:
            return equation