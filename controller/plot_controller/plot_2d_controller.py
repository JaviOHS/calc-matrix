from utils.parsers.expression_parser import ExpressionParser

class Plot2DController:
    def __init__(self, manager, figure_manager, style_helper):
        self.manager = manager
        self.figure_manager = figure_manager
        self.style_helper = style_helper
        self.parser = ExpressionParser()

    def generate_canvas(self, inputs):
        try:
            raw_expression = inputs["expression"]
            x_range = inputs["x_range"]

            if not raw_expression or not x_range:
                raise ValueError("Expresión o rango no proporcionado")
            
            if x_range[0] == x_range[1]:
                raise ValueError("El rango de x no puede ser igual.")
            
            expressions = [expr.strip() for expr in raw_expression.split(",") if expr.strip()]
            if len(expressions) > 5:
                raise ValueError("Solo se permiten hasta 5 funciones.")
                
            plot_data = self.manager.prepare_2d_data(expressions, x_range, self.parser)
            return self._create_plot(plot_data)
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica 2D:\n{str(e)}")

    def _create_plot(self, plot_data):
        canvas = self.figure_manager.create_canvas()
        ax = canvas.ax
        
        self.style_helper.apply_dark_style(canvas, ax)
        
        for idx, (expr, x_vals, y_vals) in enumerate(plot_data):
            # Manejar el caso de valores constantes
            if isinstance(y_vals, (int, float)) or len(y_vals) == 1:
                y_vals = [float(y_vals)] * len(x_vals)
            
            # Validar dimensiones
            if len(x_vals) != len(y_vals):
                raise ValueError(f"Dimensiones incompatibles para '{expr}'. "
                              f"x: {len(x_vals)}, y: {len(y_vals)}")
            
            ax.plot(x_vals, y_vals, 
                   color=self.style_helper.get_plot_color(idx),
                   linewidth=1.5,
                   label=f'f(x) = {expr}')
            
            # Agregar marcadores solo al inicio y final
            ax.plot([x_vals[0], x_vals[-1]], 
                    [y_vals[0], y_vals[-1]],
                    'o',
                    color=self.style_helper.get_plot_color(idx),
                    markersize=6)
        
        self.style_helper.configure_legend(ax)
        return canvas
