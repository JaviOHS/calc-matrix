from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from sympy import lambdify
from utils.parsers.expression_parser import ExpressionParser

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
            y_range = inputs["y_range"]  # Asegúrate de recibir y_range

            if not raw_expression or not x_range or not y_range:
                raise ValueError("Expresión o rangos no proporcionados")

            # Separar las expresiones por comas y validar que sea solo una
            expressions = [expr.strip() for expr in raw_expression.split(",") if expr.strip()]
            if len(expressions) > 1:
                raise ValueError("Solo se puede graficar una expresión a la vez en gráficos 3D.")

            # Parsear la expresión que puede tener x y y
            parsed_expr = self.parser.parse_expression(raw_expression)
            
            # Convertir la expresión simbólica a una función de Python
            f = lambdify((self.parser.x, self.parser.y), parsed_expr, "numpy")

            # Generar los valores de x y y para la gráfica 3D
            import numpy as np
            x_vals = np.linspace(x_range[0], x_range[1], 100)  # 100 puntos de x
            y_vals = np.linspace(y_range[0], y_range[1], 100)  # 100 puntos de y
            X, Y = np.meshgrid(x_vals, y_vals)
            
            try:
                Z = f(X, Y)  # Evaluamos la función
            except Exception as e:
                raise ValueError(f"Error al evaluar la función 3D: {e}")

            # Crear la gráfica 3D
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis', rstride=1, cstride=1, alpha=0.8)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_title(f"Gráfica 3D de: {raw_expression}")

            canvas = FigureCanvas(fig)
            return canvas

        except Exception as e:
            raise ValueError(f"Error al generar gráfica 3D: {str(e)}")

