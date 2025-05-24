from utils.parsers.expression_parser import ExpressionParser

class Plot3DController:
    def __init__(self, manager, figure_manager, style_helper):
        self.manager = manager
        self.figure_manager = figure_manager
        self.style_helper = style_helper
        self.parser = ExpressionParser()

    def generate_canvas(self, inputs):
        try:
            raw_expression = inputs["expression"]
            x_range = inputs["x_range"]
            y_range = inputs["y_range"]

            if not raw_expression or not x_range or not y_range:
                raise ValueError("Expresión o rangos no proporcionados.")

            expressions = [expr.strip() for expr in raw_expression.split(",")]
            if len(expressions) > 1:
                raise ValueError("Solo se puede graficar una expresión 3D a la vez.")
            
            if x_range[0] == x_range[1] or y_range[0] == y_range[1]:
                raise ValueError("Los rangos de x y y no pueden ser iguales.")

            X, Y, Z, expression = self.manager.prepare_3d_data(expressions[0], x_range, y_range, self.parser)
            return self._create_plot(X, Y, Z, expression)
            
        except Exception as e:
            raise ValueError(f"Error al generar gráfica 3D:\n{str(e)}")

    def _create_plot(self, X, Y, Z, expression):
        canvas = self.figure_manager.create_canvas(is_3d=True)
        ax = canvas.ax
        
        self.style_helper.apply_dark_style(canvas, ax, is_3d=True)
        
        # Manejar el caso de valores constantes
        from numpy import ndarray, full_like
        if isinstance(Z, (int, float)) or (isinstance(Z, ndarray) and Z.size == 1):
            constant_value = float(Z)
            Z = full_like(X, constant_value)
        
        # Validar dimensiones
        if Z.shape != X.shape or Z.shape != Y.shape:
            raise ValueError(f"Dimensiones incompatibles para '{expression}'. "
                          f"X: {X.shape}, Y: {Y.shape}, Z: {Z.shape}")
        
        surf = ax.plot_surface(X, Y, Z, 
                        cmap='plasma',
                        linewidth=0.2,
                        antialiased=True)
        
        ax.set_title(f'f(x,y) = {expression}', 
                    color=self.style_helper.TEXT_COLOR)
        
        return canvas
