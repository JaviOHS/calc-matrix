from ui.dialogs.base.base_dialog import BaseDialog
from ui.widgets.expression_components.custom_toolbar import CustomNavigationToolbar
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QSizePolicy, QHBoxLayout
from utils.components.image_utils import create_image_label

class CanvasDialog(BaseDialog):
    """Diálogo base para mostrar gráficos con canvas de matplotlib"""
    def __init__(self, title="", title_color="#7cb342", html_content=None, canvas=None, image_path=None, parent=None):
        self.html_content = html_content
        self.canvas = canvas
        self.image_path = image_path
        self.toolbar_buttons = []
        super().__init__(title, title_color, parent)
        self.finalize()
    
    def add_toolbar_buttons(self, buttons):
        """Añade botones a la toolbar. Debe llamarse antes de exec()"""
        self.toolbar_buttons = buttons or []
        
        # Si ya tenemos toolbar, actualizarla
        if hasattr(self, 'toolbar') and self.toolbar:
            for icon_name, tooltip, callback in self.toolbar_buttons:
                try:
                    self.toolbar.add_custom_button(icon_name, tooltip, callback)
                except Exception as e:
                    print(f"No se pudo añadir botón ({icon_name}): {e}")
    
    def setup_content_area(self):
        """Configura el área de contenido con HTML y/o canvas"""
        # Contenedor principal
        combined_widget = QWidget()
        combined_layout = QHBoxLayout(combined_widget)
        combined_layout.setContentsMargins(10, 10, 10, 10)
        combined_layout.setSpacing(15)
        
        # Lado izquierdo (HTML + imagen decorativa)
        if self.html_content or self.image_path:
            left_container = self._create_left_container()
            combined_layout.addWidget(left_container)
        
        # Lado derecho (Canvas con toolbar)
        if self.canvas:
            canvas_container = self._create_canvas_container()
            combined_layout.addWidget(canvas_container)
            
        # Agregar el contenedor combinado al layout principal
        self.background_layout.addWidget(combined_widget)
    
    def _create_left_container(self):
        """Crea el contenedor izquierdo con HTML y/o imagen"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Contenido HTML
        if self.html_content:
            html_display = QTextBrowser()
            html_display.setHtml(self.html_content)
            html_display.setMinimumHeight(150)
            html_display.setMinimumWidth(250)
            html_display.setOpenExternalLinks(True)
            layout.addWidget(html_display)
    
        # Añadir stretch antes de la imagen para centrar verticalmente
        if self.image_path:
            # Añadir stretch antes para empujar la imagen hacia abajo
            layout.addStretch()
            
            # Imagen decorativa
            image_label = create_image_label(self.image_path, width=128, height=128)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            # Centrar la imagen horizontalmente
            image_container = QWidget()
            image_layout = QHBoxLayout(image_container)
            image_layout.addStretch()
            image_layout.addWidget(image_label)
            image_layout.addStretch()
            
            layout.addWidget(image_container)
            
            # Añadir stretch después para empujar la imagen hacia arriba
            layout.addStretch()
            
        return container
    
    def _create_canvas_container(self):
        """Crea el contenedor del canvas con toolbar"""
        if not self.canvas:
            return QWidget()
            
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Configurar canvas
        self.canvas.setMinimumSize(500, 350)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Toolbar
        self.toolbar = CustomNavigationToolbar(self.canvas, container)
        
        # Añadir botones personalizados
        for icon_name, tooltip, callback in self.toolbar_buttons:
            try:
                self.toolbar.add_custom_button(icon_name, tooltip, callback)
            except Exception as e:
                print(f"No se pudo añadir botón ({icon_name}): {e}")
        
        # Añadir componentes al layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Renderizar el canvas
        self.canvas.draw()
        
        return container