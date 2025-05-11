from ui.dialogs.message_dialog import MessageDialog
from ui.widgets.expression_components.custom_toolbar import CustomNavigationToolbar
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QSizePolicy, QHBoxLayout
from utils.image_utils import create_image_label

class CanvasDialogManager:
    """Gestor para mostrar diálogos con canvas (gráficos) y/o resultados HTML"""
    def __init__(self, parent_widget: QWidget = None):
        self.parent_widget = parent_widget
    
    def show_canvas_dialog(self, canvas, title="🟢 GRÁFICA DE FUNCIÓN", title_color="#7cb342", image_name="success.png"):
        """Muestra un diálogo con el canvas proporcionado y barra de herramientas"""
        if not canvas:
            return
        
        # Crear un contenedor para el canvas y la barra de herramientas
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        canvas_layout.setSpacing(0)
        
        # Configura el canvas para que tenga un tamaño mínimo pero que pueda expandirse
        canvas.setMinimumSize(600, 400)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Añadir una barra de herramientas de Matplotlib
        toolbar = CustomNavigationToolbar(canvas, canvas_container)
        
        # Añadir el toolbar y el canvas al layout
        canvas_layout.addWidget(toolbar)
        canvas_layout.addWidget(canvas)
        
        canvas.draw() # Dibujar el canvas
        
        # Mostrar el diálogo con el contenedor que incluye el canvas y la barra
        dialog = MessageDialog(title=title, title_color=title_color, image_name=image_name, parent=self.parent_widget, custom_widget=canvas_container)
        dialog.exec()

    def show_result_dialog(self, html_content=None, canvas=None, title="🟢 RESULTADO", title_color="#7cb342"):
        """Muestra un diálogo combinando resultados HTML y canvas si se proporcionan"""
        if not html_content and not canvas:
            return
            
        # Crear contenedor para el contenido combinado
        combined_widget = QWidget()
        combined_layout = QHBoxLayout(combined_widget)
        combined_layout.setContentsMargins(10, 10, 10, 10)
        combined_layout.setSpacing(15)
        
        # Contenedor izquierdo para HTML y la imagen
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)
        
        # Agregar el resultado HTML si existe
        if html_content:
            html_display = QTextBrowser()
            html_display.setHtml(html_content)
            html_display.setMinimumHeight(150)
            html_display.setMinimumWidth(250)
            html_display.setOpenExternalLinks(True)
            left_layout.addWidget(html_display)
        
        # Agregar imagen debajo del HTML
        image_label = create_image_label("assets/images/dialogs/edo.png", width=200, height=200)
        image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        image_container = QWidget()
        image_layout = QHBoxLayout(image_container)
        image_layout.addStretch()
        image_layout.addWidget(image_label)
        image_layout.addStretch()
        left_layout.addWidget(image_container)
        left_layout.addStretch()
        
        # Agregar el contenedor izquierdo al layout principal
        combined_layout.addWidget(left_container)
        
        # Contenedor para el canvas con barra de herramientas
        if canvas:
            canvas_container = QWidget()
            canvas_layout = QVBoxLayout(canvas_container)
            canvas_layout.setContentsMargins(0, 0, 0, 0)
            canvas_layout.setSpacing(0)
            
            # Configurar canvas para que se expanda correctamente
            canvas.setMinimumSize(500, 350)
            canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # Agregar barra de herramientas
            toolbar = CustomNavigationToolbar(canvas, canvas_container)
            
            canvas_layout.addWidget(toolbar)
            canvas_layout.addWidget(canvas)
            
            # Dibujar el canvas
            canvas.draw()
            combined_layout.addWidget(canvas_container)
        
        # Se envía la imagen vacía ya que se está colocando directamente en el layout
        dialog = MessageDialog(title=title, title_color=title_color, image_name=None, parent=self.parent_widget, custom_widget=combined_widget)
        dialog.exec()
