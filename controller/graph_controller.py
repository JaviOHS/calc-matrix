from utils.parsers.expression_parser import ExpressionParser
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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
                
            # Delegar la lógica de evaluación al manager y modelo
            plot_data = self.manager.prepare_2d_data(expressions, x_range, self.parser)
            
            # Crear visualización con los datos procesados
            return self._create_2d_plot(plot_data)
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica 2D:\n{str(e)}")
            
    def _create_2d_plot(self, plot_data):
        # Crear figura con tamaño adecuado y más espacio para ejes
        fig, ax = plt.subplots(figsize=(10, 7))
        
        for expr, x_vals, y_vals in plot_data:
            ax.plot(x_vals, y_vals, label=f'f(x) = {expr}')

        ax.set_xlabel("x", fontsize=12)
        ax.set_ylabel("f(x)", fontsize=12)
        ax.grid(True, alpha=0.7)
        ax.set_title("Gráfica 2D", fontsize=14)
        
        # Ubicar la leyenda en posición óptima según el número de funciones
        if len(plot_data) > 2:
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=True)
        else:
            ax.legend(frameon=True)
        
        # Ajustar los márgenes manualmente - valores optimizados
        plt.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.20)
        
        return FigureCanvas(fig)

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

            # Pasar el parser al método prepare_3d_data
            X, Y, Z, expression = self.manager.prepare_3d_data(expressions[0], x_range, y_range, self.parser)
            
            # Crear visualización con los datos procesados
            return self._create_3d_plot(X, Y, Z, expression)
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica 3D:\n{str(e)}")
            
    def _create_3d_plot(self, X, Y, Z, expression):
        # Crear figura con tamaño adecuado - aumentado para mejor visualización
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', rstride=1, cstride=1, alpha=0.8)
        
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)
        ax.set_title(f"Gráfica 3D de: {expression}", fontsize=14)
        
        # Añadir barra de color con mejor posicionamiento
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, pad=0.1)
        cbar.ax.tick_params(labelsize=10)
        
        # Ajustar los márgenes manualmente - valores optimizados para 3D
        plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05)
        
        return FigureCanvas(fig)

    def generate_ode_solution_canvas(self, equation, solution_points, initial_condition=None, x_range=None, title=None):
        try:
            # Delegar procesamiento al manager
            x_vals, y_vals, eq, ic = self.manager.prepare_ode_solution(
                equation, solution_points, initial_condition, x_range
            )
            
            # Crear visualización con los datos procesados
            return self._create_ode_plot(x_vals, y_vals, eq, ic, title, x_range)
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica de solución ODE:\n{str(e)}")
            
    def _create_ode_plot(self, x_vals, y_vals, equation, initial_condition, title, x_range):
        # Crear figura con tamaño adecuado y más espacio para ejes
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Graficar la solución numérica
        ax.plot(x_vals, y_vals, 'b-o', markersize=3, label='Solución numérica')
        
        # Marcar la condición inicial
        if initial_condition:
            ax.plot(initial_condition[0], initial_condition[1], 'ro', markersize=6, label='Condición inicial')
        
        # Marcar el punto final con otro color
        if len(x_vals) > 0 and len(y_vals) > 0:
            ax.plot(x_vals[-1], y_vals[-1], 'go', markersize=6, label='Punto final')
        
        # Configurar apariencia
        ax.set_title(title if title else f"Solución de: {equation}", fontsize=14)
        ax.set_xlabel("x", fontsize=12)
        ax.set_ylabel("y", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Ubicar la leyenda en posición óptima para no interferir con la gráfica
        ax.legend(loc='best', frameon=True)
        
        # Ajustar los márgenes manualmente - valores optimizados
        plt.subplots_adjust(left=0.12, right=0.95, top=0.90, bottom=0.15)
        
        return FigureCanvas(fig)
