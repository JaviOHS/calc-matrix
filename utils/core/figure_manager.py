import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class FigureManager:
    """
    Gestor de figuras de matplotlib para evitar fugas de memoria.
    Proporciona métodos para crear, gestionar y limpiar recursos de visualización.
    """
    def __init__(self):
        self.active_figures = {}
        self.figure_count = 0
        
        # Configurar matplotlib para limitar advertencias
        plt.rcParams.update({'figure.max_open_warning': 50})
        
    def create_figure(self, figsize=(10, 7)):
        """Crea una nueva figura y la registra en el gestor."""
        fig, ax = plt.subplots(figsize=figsize)
        self.figure_count += 1
        fig_id = f"fig_{self.figure_count}"
        self.active_figures[fig_id] = fig
        return fig, ax, fig_id
        
    def create_3d_figure(self, figsize=(10, 8)):
        """Crea una figura con proyección 3D"""
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        self.figure_count += 1
        fig_id = f"fig_3d_{self.figure_count}"
        self.active_figures[fig_id] = fig
        return fig, ax, fig_id
    
    def create_canvas(self, figsize=(10, 7), is_3d=False):
        """Crea una figura y devuelve su canvas"""
        if is_3d:
            fig, ax, fig_id = self.create_3d_figure(figsize)
        else:
            fig, ax, fig_id = self.create_figure(figsize)
            
        canvas = FigureCanvas(fig)
        canvas.ax = ax
        
        # Cerrar la figura después de crear el canvas
        self.close_figure(fig_id)
        
        return canvas
    
    def close_figure(self, fig_id):
        """Cierra y elimina una figura registrada"""
        if fig_id in self.active_figures:
            plt.close(self.active_figures[fig_id])
            del self.active_figures[fig_id]
    
    def close_all(self):
        """Cierra todas las figuras registradas"""
        for fig_id in list(self.active_figures.keys()):
            self.close_figure(fig_id)
            
    def __del__(self):
        """Destructor: asegura que se liberen todos los recursos"""
        self.close_all()
        