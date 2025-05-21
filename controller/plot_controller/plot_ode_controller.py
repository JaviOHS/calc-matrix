class PlotODEController:
    def __init__(self, manager, figure_manager, style_helper):
        self.manager = manager
        self.figure_manager = figure_manager
        self.style_helper = style_helper

    def generate_solution_canvas(self, equation, solution_points, initial_condition=None, x_range=None, is_numerical=True):
        try:
            x_vals, y_vals, eq, ic = self.manager.prepare_ode_solution(
                equation, solution_points, initial_condition, x_range
            )
            return self._create_plot(x_vals, y_vals, eq, ic, x_range, is_numerical)
        except Exception as e:
            raise ValueError(f"Error al generar gráfica ODE:\n{str(e)}")

    def generate_comparison_canvas(self, equation, solutions, initial_condition=None, x_range=None, h=0.1):
        return self._create_comparison_plot(equation, solutions, initial_condition, x_range, h)

    def _create_plot(self, x_vals, y_vals, equation, initial_condition, x_range, is_numerical=True):
        canvas = self.figure_manager.create_canvas()
        ax = canvas.ax
        
        self.style_helper.apply_dark_style(canvas, ax)
        
        if is_numerical:
            # Para soluciones numéricas: mostrar todos los puntos
            ax.plot(x_vals, y_vals, 
                   color=self.style_helper.get_plot_color(0),
                   marker='.',  # punto pequeño para cada paso
                   markersize=4,
                   linestyle='-',
                   linewidth=1,
                   label=f'Solución numérica')
        else:
            # Para soluciones analíticas: solo línea continua con puntos inicial y final
            ax.plot(x_vals, y_vals, 
                   color=self.style_helper.get_plot_color(0),
                   linewidth=1.5,
                   label=f'Solución analítica')
            
            # Agregar puntos inicial y final
            ax.plot([x_vals[0], x_vals[-1]], 
                   [y_vals[0], y_vals[-1]],
                   'o',
                   color=self.style_helper.get_plot_color(0),
                   markersize=6)
        
        # Mostrar condición inicial si existe
        if initial_condition:
            x0, y0 = initial_condition
            ax.plot(x0, y0, '*', 
                   color=self.style_helper.get_plot_color(1),
                   markersize=10,
                   label=f'CI: ({x0}, {y0})')
        
        self.style_helper.configure_legend(ax)
        return canvas

    def _create_comparison_plot(self, equation, solutions, initial_condition, x_range, h):
        canvas = self.figure_manager.create_canvas()
        ax = canvas.ax
        
        self.style_helper.apply_dark_style(canvas, ax)
        
        for idx, (method, points) in enumerate(solutions.items()):
            x_vals, y_vals = zip(*points)
            
            # Usar un estilo especial para la solución analítica
            if method == "analytical":
                ax.plot(x_vals, y_vals,
                    color='white',  # Color diferente para la solución analítica
                    linestyle='-',
                    linewidth=1,
                    label='Solución Analítica')
            else:
                ax.plot(x_vals, y_vals,
                    color=self.style_helper.get_plot_color(idx),
                    marker='.',     # Punto pequeño para cada paso
                    markersize=4,
                    linestyle='-',
                    linewidth=1,
                    label=f'{method}')
        
        # Mostrar condición inicial si existe
        if initial_condition:
            x0, y0 = initial_condition
            ax.plot(x0, y0, '*', 
                color='yellow',  # Color diferente para destacar
                markersize=10,
                label=f'CI: ({x0}, {y0})')
        
        self.style_helper.configure_legend(ax)
        return canvas
