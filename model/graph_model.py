from sympy import lambdify
from numpy import linspace, meshgrid

class GraphModel:
    def __init__(self, expressions=None, x_range=None, y_range=None):
        self.expressions = expressions if expressions else []
        if x_range:
            self.x_min, self.x_max = x_range
        if y_range:
            self.y_min, self.y_max = y_range

    def evaluate_2d_function(self, parsed_expr, x_symbol, num_points=500):
        """Evalúa una expresión 2D en el rango definido"""
        x_vals = linspace(self.x_min, self.x_max, num_points)
        f = lambdify(x_symbol, parsed_expr, "numpy")
        try:
            y_vals = f(x_vals)
            return x_vals, y_vals
        except Exception as e:
            raise ValueError(f"Error evaluando la función 2D:\n{e}")

    def evaluate_3d_function(self, parsed_expr, x_symbol, y_symbol, num_points=100):
        """Evalúa una expresión 3D en los rangos definidos"""
        x_vals = linspace(self.x_min, self.x_max, num_points)
        y_vals = linspace(self.y_min, self.y_max, num_points)
        X, Y = meshgrid(x_vals, y_vals)
        
        f = lambdify((x_symbol, y_symbol), parsed_expr, modules="numpy")
        try:
            Z = f(X, Y)
            return X, Y, Z
        except Exception as e:
            raise ValueError(f"Error evaluando la función 3D:\n{e}")
            
    def prepare_ode_solution(self, solution_points):
        """Prepara los datos para graficar una solución de ODE"""
        try:
            x_vals, y_vals = zip(*solution_points)
            return x_vals, y_vals
        except Exception as e:
            raise ValueError(f"Error preparando datos de ODE:\n{e}")
