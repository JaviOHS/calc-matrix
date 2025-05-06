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

            # Parsear la expresión
            parsed_expr = self.parser.parse_expression(raw_expression)
            
            # Convertir la expresión simbólica a una función de Python
            f = lambdify(self.parser.x, parsed_expr, "numpy")

            # Generar los valores de x para la gráfica
            import numpy as np
            x_vals = np.linspace(x_range[0], x_range[1], 500)  # Generamos 500 puntos de x
            y_vals = f(x_vals)  # Evaluamos la función para esos puntos

            # Crear la gráfica
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label=f'f(x) = {raw_expression}')
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.set_title("Gráfica 2D de la función")
            ax.legend()

            canvas = FigureCanvas(fig)
            return canvas

        except Exception as e:
            raise ValueError(f"Error al generar gráfica 2D: Asegúrese de que la expresión sea válida.")

    def generate_canvas_3d(self, inputs):
        try:
            raw_expression = inputs["expression"]
            x_range = inputs["x_range"]
            y_range = inputs["y_range"]  # Asegúrate de recibir y_range

            if not raw_expression or not x_range or not y_range:
                raise ValueError("Expresión o rangos no proporcionados")

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
                raise ValueError(f"Error al evaluar la función: {e}")

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
