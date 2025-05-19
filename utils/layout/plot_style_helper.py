class PlotStyleHelper:
    def __init__(self):
        # Colores base
        self.BACKGROUND_COLOR = '#0F161F'
        self.AXIS_BACKGROUND = '#0F161F'
        self.TEXT_COLOR = '#D8DEE9'
        
        # Paleta de colores para gráficas
        self.PLOT_COLORS = [
            '#ff8103',  # Naranja principal
            '#50fa7b',  # Verde neón
            '#ff4d4d',  # Rojo brillante
            '#bd93f9',  # Púrpura
            '#8be9fd',  # Cyan
            '#ffb86c'   # Naranja claro
        ]
        
        self.MARKERS = ['o', 's', 'd', '^', 'v', 'p']

    def apply_dark_style(self, canvas, ax, is_3d=False):
        """Aplica el estilo oscuro base a cualquier gráfica"""
        canvas.figure.patch.set_facecolor(self.BACKGROUND_COLOR)
        ax.set_facecolor(self.AXIS_BACKGROUND)
        
        # Configurar colores de los ejes
        if is_3d:
            self._configure_3d_style(ax)
        else:
            self._configure_2d_style(ax)

    def _configure_2d_style(self, ax):
        """Configura el estilo para gráficas 2D"""
        for spine in ax.spines.values():
            spine.set_color(self.TEXT_COLOR)
            
        ax.tick_params(axis='both', colors=self.TEXT_COLOR)
        ax.grid(True, alpha=0.2, color=self.TEXT_COLOR)

    def _configure_3d_style(self, ax):
        """Configura el estilo para gráficas 3D"""
        ax.xaxis.set_pane_color((0.11, 0.17, 0.26, 1.0))
        ax.yaxis.set_pane_color((0.11, 0.17, 0.26, 1.0))
        ax.zaxis.set_pane_color((0.11, 0.17, 0.26, 1.0))
        
        for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
            axis._axinfo["grid"]["color"] = (0.85, 0.87, 0.91, 0.1)
            axis.set_tick_params(colors=self.TEXT_COLOR)

    def configure_legend(self, ax, **kwargs):
        """Configura el estilo de la leyenda"""
        default_props = {
            'frameon': True,
            'facecolor': self.AXIS_BACKGROUND,
            'edgecolor': self.TEXT_COLOR,
            'labelcolor': self.TEXT_COLOR
        }
        legend_props = {**default_props, **kwargs}
        ax.legend(**legend_props)

    def get_plot_color(self, index):
        """Obtiene un color de la paleta"""
        return self.PLOT_COLORS[index % len(self.PLOT_COLORS)]

    def get_marker(self, index):
        """Obtiene un marcador de la lista"""
        return self.MARKERS[index % len(self.MARKERS)]
    