from model.graph_model import GraphModel
import sympy

class GraphManager:
    def __init__(self):
        self.current_model = GraphModel()
        
    def prepare_2d_data(self, expressions, x_range, parser):
        """Prepara los datos para una gráfica 2D"""
        self.current_model = GraphModel(expressions, x_range)
        results = []
        
        for expr in expressions:
            parsed_expr = parser.parse_expression(expr)
            x_vals, y_vals = self.current_model.evaluate_2d_function(parsed_expr, parser.x)
            results.append((expr, x_vals, y_vals))
            
        return results
        
    def prepare_3d_data(self, expression, x_range, y_range, parser):
        """Prepara los datos para una gráfica 3D usando el mismo parser que 2D"""
        self.current_model = GraphModel([expression], x_range, y_range)
        
        # Usar parser.parse_expression como en prepare_2d_data
        x, y = sympy.symbols('x y')
        
        try:
            # Usar el mismo método de parseo que en 2D
            parsed_expr = parser.parse_expression(expression, use_3d=True)
            
            # Evaluar la función 3D
            X, Y, Z = self.current_model.evaluate_3d_function(parsed_expr, x, y)
            return X, Y, Z, expression
        except Exception as e:
            raise ValueError(f"Error preparando datos 3D:\n{e}")
            
    def prepare_ode_solution(self, equation, solution_points, initial_condition=None, x_range=None):
        """Prepara datos para graficar una solución de ODE"""
        self.current_model = GraphModel(None, x_range) if x_range else GraphModel()
        x_vals, y_vals = self.current_model.prepare_ode_solution(solution_points)
        return x_vals, y_vals, equation, initial_condition
        
    def get_model(self):
        return self.current_model

    def clear(self):
        self.current_model = GraphModel()
