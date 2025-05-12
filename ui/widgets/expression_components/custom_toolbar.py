from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from utils.action_buttons import ActionButton

class CustomNavigationToolbar(NavigationToolbar2QT):
    """Barra de herramientas personalizada de Matplotlib"""
    toolitems = [t for t in NavigationToolbar2QT.toolitems if t[0] in ('Home', 'Pan', 'Save')]

    def __init__(self, canvas, parent=None, coordinates=True):
        super().__init__(canvas, parent, coordinates)
        
        # Diccionario de tooltips estándar y extendidos
        tooltips = {
            'home': ("Restablecer vista original", "Vuelve a la vista inicial del gráfico"),
            'pan': ("Desplazar vista", "Permite arrastrar el gráfico para ver diferentes áreas"),
            'save_figure': ("Guardar gráfico", "Guarda la gráfica como imagen PNG, JPG, SVG o PDF")
        }
        
        # Añadir botones personalizados con tooltips
        if 'home' in self._actions:
            home_button = ActionButton.icon_only("reset.svg", parent=self)
            home_button.setToolTip(tooltips['home'][0])
            home_button.setStatusTip(tooltips['home'][1])
            home_button.clicked.connect(self.home)
            self.addWidget(home_button)
            self._remove_action('home')
        
        if 'pan' in self._actions:
            pan_button = ActionButton.icon_only("move.svg", parent=self)
            pan_button.setToolTip(tooltips['pan'][0])
            pan_button.setStatusTip(tooltips['pan'][1])
            pan_button.clicked.connect(self.pan)
            self.addWidget(pan_button)
            self._remove_action('pan')
        
        if 'save_figure' in self._actions:
            save_button = ActionButton.icon_only("save.svg", parent=self)
            save_button.setToolTip(tooltips['save_figure'][0])
            save_button.setStatusTip(tooltips['save_figure'][1])
            save_button.clicked.connect(self.save_figure)
            self.addWidget(save_button)
            self._remove_action('save_figure')

    def _remove_action(self, action_name):
        """Eliminar una acción de la barra de herramientas."""
        action = self._actions.get(action_name)
        if action:
            self.removeAction(action)
    
    def add_custom_button(self, icon_name, tooltip, callback):
        """Añade un botón personalizado a la barra de herramientas."""
        button = ActionButton.icon_only(icon_name, parent=self)
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        self.addWidget(button)
        return button