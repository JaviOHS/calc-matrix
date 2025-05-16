from sympy.parsing.sympy_parser import standard_transformations,implicit_multiplication_application,convert_xor,implicit_application,parse_expr
from model.polynomial_model import Polynomial
from utils.validators import exponents_validator, validate_characters, validate_parentheses,validate_symbols,validate_expression_syntax
from utils.patterns import MATH_SYMBOLS, ODE_PATTERNS, SPECIAL_CHARS, ALLOWED_CHARS, ALLOWED_DIFFERENTIAL_CHARS
import sympy as sp
import re
import numpy as np

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

        # Nombres permitidos para la validación de símbolos
        self.allowed_names = set(self.common_symbols.keys()) | {"x", "y", "dx", "dy"}

        # Usar ambos conjuntos de caracteres
        self.allowed_chars = ALLOWED_CHARS
        self.allowed_differential_chars = ALLOWED_DIFFERENTIAL_CHARS
        self.special_chars_map = SPECIAL_CHARS

    def sanitize_expression(self, expr: str, use_3d=False) -> str:
        """
        Sanitiza la expresión matemática para evitar errores de sintaxis.
        Reemplaza caracteres especiales y ajusta la notación.
        """
        # Aplicar reemplazos básicos
        for bad, good in MATH_SYMBOLS.items():
            expr = expr.replace(bad, good)

        # Solo aplicar reemplazos específicos de EDO si no estamos en modo 3D
        if not use_3d:
            for pattern, replacement in ODE_PATTERNS.items():
                expr = re.sub(pattern, replacement, expr)

        return expr

    def validate_expression_symbols(self, expr: str, use_3d=False, is_differential=False):
        """Wrapper para la validación de símbolos"""
        is_valid, error_msg = validate_symbols(
            expr, 
            self.allowed_names, 
            use_3d, 
            is_differential
        )
        if not is_valid:
            raise ValueError(error_msg)

    def parse_expression(self, raw_expr: str, use_3d=False, max_length: int = 500, is_differential=False):
        """Analiza una expresión matemática y la convierte a formato sympy"""
        try:
            if not raw_expr.strip():
                raise ValueError("La expresión está vacía")
                
            if len(raw_expr) > max_length:
                raise ValueError(f"La expresión es demasiado larga (máximo: {max_length} caracteres)")

            # Validar sintaxis básica antes de sanitizar
            is_valid, error_msg = validate_expression_syntax(raw_expr)
            if not is_valid:
                raise ValueError(error_msg)

            # Sanitizar y validar la expresión
            clean_expr = self.sanitize_expression(raw_expr, use_3d)
            self.validate_expression_symbols(clean_expr, use_3d, is_differential)
            
            # Seleccionar el conjunto de símbolos apropiado
            allowed_symbols = self.allowed_symbols_3d if (use_3d or is_differential) else self.allowed_symbols_2d
            
            parsed = parse_expr(clean_expr, 
                              transformations=self.transformations, 
                              local_dict=allowed_symbols)
            
            # Evaluar si la expresión es una constante
            if parsed.is_constant():
                return float(parsed.evalf())
            
            return sp.expand(parsed)
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            error_msg = str(e).lower()
            if "name 'y' is not defined" in error_msg:
                raise ValueError("La variable 'y' solo está permitida en gráficas 3D y ecuaciones diferenciales.")
            elif "multiply sequence" in error_msg or "can't multiply sequence" in error_msg:
                raise ValueError("Expresión mal formada. Use · para multiplicación explícita entre términos.")
            elif "invalid syntax" in error_msg:
                raise ValueError("Sintaxis inválida en la expresión")
            else:
                raise ValueError(f"Error al procesar la expresión: {str(e)}")

    def to_polynomial(self, sympy_expr):
        """Convierte una expresión sympy a un objeto Polynomial."""
        try:
            poly_expr = sp.Poly(sympy_expr, self.x, domain='QQ')
            coeffs = poly_expr.all_coeffs()
            return Polynomial([sp.Rational(c) for c in coeffs])
        except ValueError:
            raise ValueError("La expresión no representa un polinomio válido. Asegúrese de que la expresión contenga sólo potencias enteras de x con coeficientes numéricos.")
        except Exception:
            raise ValueError("Hubo un error al intentar convertir la expresión en un polinomio. Verifique la expresión.")
       
    def parse_equation(self, raw_expr: str):
        """Parsea una ecuación y la convierte en una expresión sympy Eq."""
        try:
            # Validaciones básicas primero
            if len(raw_expr) > 500:
                raise ValueError("La expresión es demasiado larga (máximo: 500 caracteres)")

            if not exponents_validator(raw_expr):
                raise ValueError("El exponente es demasiado alto... (máximo: 1000)")
                
            # Para ecuaciones, siempre permitir caracteres diferenciales
            # ya que representan EDOs donde la comilla simple es válida
            chars_to_validate = self.allowed_differential_chars
                
            # Validar caracteres y paréntesis
            is_valid, error_msg = validate_characters(raw_expr, chars_to_validate, self.special_chars_map)
            if not is_valid:
                raise ValueError(error_msg)
                
            is_valid, error_msg = validate_parentheses(raw_expr)
            if not is_valid:
                raise ValueError(error_msg)

            # Validar símbolos permitidos
            self.validate_expression_symbols(raw_expr, is_differential=True)
            
            # Sanitizar la expresión
            clean_expr = self.sanitize_expression(raw_expr)
                
            # Manejar el caso especial donde ya viene como Eq
            if clean_expr.startswith("Eq("):
                return parse_expr(clean_expr, local_dict=self.allowed_symbols_2d)
                
            # Dividir en LHS y RHS
            if '==' in clean_expr:
                lhs, rhs = clean_expr.split('==', 1)
                lhs_expr = parse_expr(lhs.strip(), transformations=self.transformations, 
                                    local_dict=self.allowed_symbols_2d)
                rhs_expr = parse_expr(rhs.strip(), transformations=self.transformations, 
                                    local_dict=self.allowed_symbols_2d)
                return sp.Eq(lhs_expr, rhs_expr)
            else:
                # Si no hay igual, asumir == 0
                expr = parse_expr(clean_expr, transformations=self.transformations, 
                                local_dict=self.allowed_symbols_2d)
                return sp.Eq(expr, 0)
                
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            if "invalid syntax" in str(e):
                raise ValueError("Sintaxis inválida. Verifique que la expresión esté bien formada.")
            raise ValueError(f"Error al procesar la expresión: {str(e)}")
        
    def parse_ode_for_numerical(self, raw_expr: str):
        """
        Parsea una ecuación diferencial de la forma dy/dx = f(x, y)
        y devuelve una función lambda f(x, y) para métodos numéricos.
        """
        try:
            # Eliminar espacios innecesarios y asegurarse de que hay RHS
            raw_expr = raw_expr.strip()
            if raw_expr.endswith('='):
                raw_expr += '0'
                
            # Validar usando el conjunto de caracteres para diferenciales
            is_valid, error_msg = validate_characters(raw_expr, self.allowed_differential_chars, self.special_chars_map)
            if not is_valid:
                raise ValueError(error_msg)

            # Normalizar notaciones y espacios, sin convertir a Derivative()
            preprocessed_expr = self._preprocess_ode_expression(raw_expr)

            # Extraer solo el lado derecho (f(x, y))
            rhs_expr = self._extract_rhs_from_equation(preprocessed_expr)

            # Sanitizar solo el RHS (evita errores con y(x) en modo 3D)
            rhs_clean = self.sanitize_expression(rhs_expr, use_3d=True)

            # Parsear solo el RHS como función de x e y
            parsed_expr = self.parse_expression(rhs_clean, use_3d=True, is_differential=True)

            # Crear función lambda evaluable f(x, y) con manejo de errores
            def safe_lambdify(x, y):
                try:
                    result = sp.lambdify([self.x, self.y_symbol], parsed_expr, modules=['numpy'])(x, y)
                    if not np.isfinite(result):
                        raise OverflowError("Resultado numérico fuera de rango")
                    return result
                except OverflowError:
                    raise ValueError("Resultado numérico fuera de rango durante la evaluación de la ecuación diferencial.")
            
            return safe_lambdify, rhs_clean

        except Exception as e:
            raise ValueError(f"Error al analizar la ecuación diferencial: {str(e)}")

    def _preprocess_ode_expression(self, expr: str):
        """
        Normaliza la ecuación sin convertirla a Derivative,
        para evitar errores al parsear en modo 3D.
        """
        expr = re.sub(r'd\s*y\s*/\s*d\s*x', 'dy/dx', expr)
        expr = re.sub(r'Δ', 'd', expr)  # En caso de copiar y pegar símbolos raros
        return expr

    def _extract_rhs_from_equation(self, equation: str) -> str:
        """
        Extrae el lado derecho (RHS) de una ecuación del tipo dy/dx = ...
        Si no hay '=', se asume que la entrada ya es el RHS.
        """
        equation = equation.strip()

        if '=' in equation:
            lhs, rhs = equation.split('=', 1)
            rhs = rhs.strip()
            return rhs or '0'
        else:
            # Ya viene solo como RHS
            return equation
