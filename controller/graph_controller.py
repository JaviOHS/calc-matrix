from utils.parsers.expression_parser import ExpressionParser
from utils.figure_manager import FigureManager

class GraphController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()
        self.figure_manager = FigureManager()

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
        # Usar figure_manager para crear canvas y eje
        canvas, ax = self.figure_manager.create_canvas(figsize=(10, 7))
        
        # Configurar estilo oscuro
        canvas.figure.patch.set_facecolor('#0F161F')
        ax.set_facecolor('#1C2C42')
        
        for expr, x_vals, y_vals in plot_data:
            ax.plot(x_vals, y_vals, label=f'f(x) = {expr}', linewidth=2)

        ax.set_xlabel("x", fontsize=12, color='#D8DEE9')
        ax.set_ylabel("f(x)", fontsize=12, color='#D8DEE9')
        ax.grid(True, alpha=0.2, color='#D8DEE9')
        ax.set_title("Gráfica 2D", fontsize=14, color='#D8DEE9')
        
        # Configurar colores de los ejes
        ax.spines['bottom'].set_color('#D8DEE9')
        ax.spines['top'].set_color('#D8DEE9') 
        ax.spines['right'].set_color('#D8DEE9')
        ax.spines['left'].set_color('#D8DEE9')
        ax.tick_params(axis='x', colors='#D8DEE9')
        ax.tick_params(axis='y', colors='#D8DEE9')
        
        if len(plot_data) > 2:
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), 
                     ncol=3, frameon=True, facecolor='#1C2C42', 
                     edgecolor='#D8DEE9', labelcolor='#D8DEE9')
        else:
            ax.legend(frameon=True, facecolor='#1C2C42', 
                     edgecolor='#D8DEE9', labelcolor='#D8DEE9')
        
        return canvas

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
        canvas, ax = self.figure_manager.create_canvas(figsize=(10, 8), is_3d=True)
        
        # Configurar estilo oscuro
        canvas.figure.patch.set_facecolor('#0F161F')
        ax.set_facecolor('#0f161f')
        
        # Configurar color de fondo para todos los paneles
        ax.xaxis.set_pane_color((0.11, 0.17, 0.26, 1.0))  # Convertir #1C2C42 a RGB
        ax.yaxis.set_pane_color((0.11, 0.17, 0.26, 1.0))
        ax.zaxis.set_pane_color((0.11, 0.17, 0.26, 1.0))
        
        # Configurar color de las líneas de la grilla
        ax.xaxis._axinfo["grid"]["color"] = (0.85, 0.87, 0.91, 0.1)  # #D8DEE9 con alfa 0.1
        ax.yaxis._axinfo["grid"]["color"] = (0.85, 0.87, 0.91, 0.1)
        ax.zaxis._axinfo["grid"]["color"] = (0.85, 0.87, 0.91, 0.1)
        
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', rstride=1, cstride=1, alpha=0.8)
        
        ax.set_xlabel('X', fontsize=12, color='#D8DEE9')
        ax.set_ylabel('Y', fontsize=12, color='#D8DEE9')
        ax.set_zlabel('Z', fontsize=12, color='#D8DEE9')
        ax.set_title(f"Gráfica 3D de: {expression}", fontsize=14, color='#D8DEE9')
        
        # Configurar colores de los ejes
        ax.tick_params(axis='x', colors='#D8DEE9')
        ax.tick_params(axis='y', colors='#D8DEE9')
        ax.tick_params(axis='z', colors='#D8DEE9')
        
        # Colorbar con estilo oscuro
        cbar = canvas.figure.colorbar(surf, ax=ax, shrink=0.5, aspect=5, pad=0.1)
        cbar.ax.yaxis.set_tick_params(color='#D8DEE9')
        cbar.ax.yaxis.label.set_color('#D8DEE9')
        
        return canvas

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
        canvas, ax = self.figure_manager.create_canvas(figsize=(10, 7))
        
        # Configurar estilo oscuro
        canvas.figure.patch.set_facecolor('#0F161F')
        ax.set_facecolor('#1C2C42')
        
        # Graficar con colores más vibrantes
        ax.plot(x_vals, y_vals, color='#ff8103', marker='o', 
                markersize=3, label='Solución numérica', linewidth=2)
        
        if initial_condition:
            ax.plot(initial_condition[0], initial_condition[1], 
                    marker='o', markersize=6, 
                    label='Condición inicial', 
                    color='#ff4d4d')
        
        if len(x_vals) > 0 and len(y_vals) > 0:
            ax.plot(x_vals[-1], y_vals[-1], 
                    marker='o', markersize=6, 
                    label='Punto final', 
                    color='#50fa7b')
        
        # Calcular número de puntos
        num_points = len(x_vals)
        
        # Formatear título con ecuación y número de puntos
        plot_title = f"{equation} - {num_points} puntos"
        
        ax.set_title(plot_title, fontsize=14, color='#D8DEE9')
        ax.grid(True, linestyle='--', alpha=0.2, color='#D8DEE9')
        
        # Configurar colores de los ejes
        ax.spines['bottom'].set_color('#D8DEE9')
        ax.spines['top'].set_color('#D8DEE9')
        ax.spines['right'].set_color('#D8DEE9')
        ax.spines['left'].set_color('#D8DEE9')
        ax.tick_params(axis='x', colors='#D8DEE9')
        ax.tick_params(axis='y', colors='#D8DEE9')
        
        ax.legend(loc='best', frameon=True, facecolor='#1C2C42', 
                 edgecolor='#D8DEE9', labelcolor='#D8DEE9')
        
        return canvas

    def generate_ode_comparison_canvas(self, equation, solutions, initial_condition=None, x_range=None, h=0.1, method_names=None):
        canvas, ax = self.figure_manager.create_canvas(figsize=(12, 8))
        
        # Configurar estilo oscuro
        canvas.figure.patch.set_facecolor('#0F161F')
        ax.set_facecolor('#1C2C42')
        
        # Nueva paleta de colores más vibrante
        colors = ['#ff8103',  # Naranja principal
                  '#50fa7b',  # Verde neón
                  '#ff4d4d',  # Rojo brillante
                  '#bd93f9',  # Púrpura
                  '#8be9fd',  # Cyan
                  '#ffb86c']  # Naranja claro
        
        markers = ['o', 's', 'd', '^', 'v', 'p']
        
        # Formatear ecuación para el título
        equation_formatted = self._format_equation_for_display(equation)
        
        # Iterar sobre cada solución numérica
        for i, (method, solution_points) in enumerate(solutions.items()):
            # Soluciones numéricas con marcadores
            x_vals, y_vals = zip(*solution_points)
            color_idx = i % len(colors)
            marker = markers[color_idx] if i < len(markers) else 'o'
            
            # Obtener nombre descriptivo del método y número de puntos
            num_points = len(x_vals)
            method_label = f"{method_names.get(method, method)} ({num_points} pts)"
            
            # Graficar con menos marcadores para mayor claridad
            ax.plot(x_vals, y_vals, color=colors[color_idx], marker=marker, 
                    markevery=max(1, len(x_vals)//15), markersize=6, 
                    linewidth=2, label=method_label)
        
        # Marcar la condición inicial
        if initial_condition:
            ax.plot(initial_condition[0], initial_condition[1], 'ko', markersize=8, label='Condición inicial')
        
        # Configurar apariencia
        ax.set_title(equation_formatted, fontsize=14, color='#D8DEE9')
        ax.set_xlabel("x", fontsize=12, color='#D8DEE9')
        ax.set_ylabel("y(x)", fontsize=12, color='#D8DEE9')
        ax.grid(True, linestyle='--', alpha=0.2, color='#D8DEE9')
        
        # Configurar colores de los ejes
        ax.spines['bottom'].set_color('#D8DEE9')
        ax.spines['top'].set_color('#D8DEE9')
        ax.spines['right'].set_color('#D8DEE9')
        ax.spines['left'].set_color('#D8DEE9')
        ax.tick_params(axis='x', colors='#D8DEE9')
        ax.tick_params(axis='y', colors='#D8DEE9')
        
        # Información adicional
        self._add_info_text(ax, h, x_range)
        
        # Leyenda con mejor formato
        ax.legend(loc='best', frameon=True, fontsize=10,
                 facecolor='#1C2C42', edgecolor='#D8DEE9', 
                 labelcolor='#D8DEE9')
        
        return canvas

    def _format_equation_for_display(self, equation):
        """Formatea la ecuación para mostrarla en el título de la gráfica"""
        if not equation:
            return "y'"
            
        if '=' in equation:
            eq_parts = equation.split('=')
            if eq_parts[0].strip() in ["y'", "dy/dx"]:
                return f"y'(x) = {eq_parts[1].strip()}"
            else:
                return equation
        else:
            return f"y'(x) = {equation.strip()}"
        
    def _add_info_text(self, ax, h, x_range):
        """Añade texto informativo sobre los parámetros de la simulación"""
        if x_range:
            info_text = f"Paso h={h}, x∈[{x_range[0]}, {x_range[1]}]"
            ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
