from utils.parsers.expression_parser import ExpressionParser
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from sympy import lambdify
import matplotlib.pyplot as plt
import sympy as sp

class GraphController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def execute_operation(self, operation_type, inputs):
        if operation_type == "graficas_2d":
            return self.generate_canvas_2d(inputs)
        elif operation_type == "graficas_3d":
            return self.generate_canvas_3d(inputs)
        else:
            raise ValueError("Tipo de operación no soportado")

    def generate_canvas_2d(self, inputs):
        try:
            raw_expression = inputs["expression"]
            x_range = inputs["x_range"]

            if not raw_expression or not x_range:
                raise ValueError("Expresión o rango no proporcionado")

            # Separar múltiples expresiones por coma y limitar a 5
            expressions = [expr.strip() for expr in raw_expression.split(",") if expr.strip()]
            if len(expressions) > 5:
                raise ValueError("Solo se permiten hasta 5 funciones.")

            import numpy as np
            x_vals = np.linspace(x_range[0], x_range[1], 500)

            fig, ax = plt.subplots()

            for expr in expressions:
                parsed_expr = self.parser.parse_expression(expr)
                f = lambdify(self.parser.x, parsed_expr, "numpy")
                try:
                    y_vals = f(x_vals)
                    ax.plot(x_vals, y_vals, label=f'f(x) = {expr}')
                except Exception as e:
                    raise ValueError(f"Error al evaluar la función '{expr}': {e}")

            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.set_title("Gráficas 2D")
            ax.legend()

            canvas = FigureCanvas(fig)
            return canvas

        except Exception as e:
            raise ValueError(f"Error al generar gráfica 2D: {str(e)}")

    def generate_canvas_3d(self, inputs):
        try:
            raw_expression = inputs["expression"]
            x_range = inputs["x_range"]
            y_range = inputs["y_range"]

            if not raw_expression or not x_range or not y_range:
                raise ValueError("Expresión o rangos no proporcionados")

            # Separar las expresiones y validar
            expressions = [expr.strip() for expr in raw_expression.split(",") if expr.strip()]
            if len(expressions) > 1:
                raise ValueError("Solo se puede graficar una expresión a la vez en gráficos 3D.")

            # Reemplazar manualmente cualquier exponenciación para asegurar formato correcto
            expression = expressions[0].replace("^", "**")

            # Crear símbolos sympy para x e y
            x, y = sp.symbols('x y')
            
            # Parsear la expresión directamente con sympy
            try:
                parsed_expr = sp.sympify(expression)
            except Exception as e:
                raise ValueError(f"Error al parsear la expresión con sympy: {e}")
            
            # Crear una función lambda que acepte arrays de NumPy
            f = sp.lambdify((x, y), parsed_expr, modules="numpy")
            
            # Generar valores para X e Y
            import numpy as np
            x_vals = np.linspace(x_range[0], x_range[1], 100)
            y_vals = np.linspace(y_range[0], y_range[1], 100)
            X, Y = np.meshgrid(x_vals, y_vals)
            
            # Evaluar la función
            try:
                Z = f(X, Y)
            except Exception as e:
                raise ValueError(f"Error al evaluar la función con los valores: {e}")

            # Crear la figura
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
            
            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(X, Y, Z, cmap='viridis', rstride=1, cstride=1, alpha=0.8)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f"Gráfica 3D de: {raw_expression}")
            
            canvas = FigureCanvas(fig)
            return canvas
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica 3D: {str(e)}")
    
    def generate_ode_solution_canvas(self, equation, solution_points, initial_condition=None, x_range=None, title=None):
        """
        Genera un canvas con la solución gráfica de una ecuación diferencial.
        
        Args:
            equation: String representando la ecuación diferencial (para el título)
            solution_points: Lista de tuplas (x, y) con los puntos de solución
            initial_condition: Tupla (x0, y0) de la condición inicial
            x_range: Rango de x para mostrar en la gráfica
            title: Título personalizado (opcional)
        
        Returns:
            Un objeto FigureCanvas de matplotlib
        """
        try:
            # Extraer los puntos x, y
            x_vals, y_vals = zip(*solution_points)
            
            # Crear la figura y ejes
            fig, ax = plt.subplots()
            
            # Graficar la solución numérica
            ax.plot(x_vals, y_vals, 'b-o', markersize=3, label='Solución numérica')
            
            # Marcar la condición inicial
            if initial_condition:
                ax.plot(initial_condition[0], initial_condition[1], 'ro', markersize=6, label='Condición inicial')
            
            # Configurar apariencia
            ax.set_title(title if title else f"Solución de: {equation}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.legend()
            
            # Ajustar los límites del eje x si se proporciona un rango
            if x_range:
                ax.set_xlim(x_range)
            
            # Crear el canvas para Qt
            canvas = FigureCanvas(fig)
            return canvas
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica de solución ODE: {str(e)}")