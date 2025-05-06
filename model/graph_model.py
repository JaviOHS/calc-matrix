import numpy as np
import sympy
from sympy import lambdify

class GraphModel:
    def __init__(self, expressions, x_range, y_range=None):
        if isinstance(expressions, str):
            expressions = [expressions]
        self.expressions = expressions
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range if y_range else x_range

    def evaluate_function(self):
        x = np.linspace(self.x_min, self.x_max, 400)
        try:
            y = eval(self.expression, {"x": x, "np": np, "__builtins__": {}})
            return x, y
        except Exception as e:
            raise ValueError(f"Error evaluando la función: {e}")

    def evaluate_function_3d(self):
        if not hasattr(self, 'y_min') or not hasattr(self, 'y_max'):
            raise ValueError("Se requieren rangos para X e Y en gráficas 3D")
            
        x_vals = np.linspace(self.x_min, self.x_max, 100)
        y_vals = np.linspace(self.y_min, self.y_max, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        try:
            parsed_expr = sympy.sympify(self.expression)
            f = lambdify(('x', 'y'), parsed_expr, 'numpy')
            Z = f(X, Y)
            return X, Y, Z
        except Exception as e:
            raise ValueError(f"Error evaluando la función 3D: {e}")
        