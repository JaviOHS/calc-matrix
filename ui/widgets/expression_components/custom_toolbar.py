from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from utils.action_buttons import ActionButton  

class CustomNavigationToolbar(NavigationToolbar2QT):
    """Barra de herramientas personalizada de Matplotlib"""
    toolitems = [t for t in NavigationToolbar2QT.toolitems if t[0] in ('Home', 'Pan', 'Save')]

    def __init__(self, canvas, parent=None, coordinates=True):
        super().__init__(canvas, parent, coordinates)
        
        if 'home' in self._actions:
            home_button = ActionButton.icon_only("reset.svg", parent=self)
            home_button.clicked.connect(self.home)
            self.addWidget(home_button)
            self._remove_action('home')
        
        if 'pan' in self._actions:
            pan_button = ActionButton.icon_only("move.svg", parent=self)
            pan_button.clicked.connect(self.pan)
            self.addWidget(pan_button)
            self._remove_action('pan')
        
        if 'save_figure' in self._actions:
            save_button = ActionButton.icon_only("save.svg", parent=self)
            save_button.clicked.connect(self.save_figure)
            self.addWidget(save_button)
            self._remove_action('save_figure')

    def _remove_action(self, action_name):
        """Eliminar una acción de la barra de herramientas."""
        action = self._actions.get(action_name)
        if action:
            self.removeAction(action)
