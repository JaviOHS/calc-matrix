from ui.dialogs.message_dialog import MessageDialog
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from utils.resources import resource_path
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtWidgets import QHBoxLayout, QLabel

class CanvasDialogManager:
    """Gestor para mostrar diálogos con canvas (gráficos) y/o resultados HTML"""
    
    def __init__(self, parent_widget: QWidget = None):
        self.parent_widget = parent_widget
    
    def show_canvas_dialog(self, canvas, title="🟢 GRÁFICA DE FUNCIÓN", title_color="#7cb342", image_name="success.png"):
        """Muestra un diálogo con el canvas proporcionado"""
        if not canvas:
            return
            
        canvas.setFixedSize(500, 300)
        canvas.draw()
        dialog = MessageDialog(title=title, title_color=title_color, image_name=image_name, parent=self.parent_widget, custom_widget=canvas)
        dialog.exec()

    def show_result_dialog(self, html_content=None, canvas=None, title="🟢 RESULTADO", title_color="#7cb342"):
        """Muestra un diálogo combinando resultados HTML y canvas si se proporcionan"""
        if not html_content and not canvas:
            return
            
        # Crear contenedor para el contenido combinado
        combined_widget = QWidget()
        combined_layout = QHBoxLayout(combined_widget)  # Cambio a QHBoxLayout para disposición horizontal
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
        
        # Agregar imagen success.png debajo del HTML
        image_path = resource_path("assets/images/dialogs/edo.png")
        pixmap = QPixmap(image_path).scaled(164, 164, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
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
        
        # Agregar el canvas a la derecha si existe
        if canvas:
            canvas.setMinimumSize(500, 300)
            canvas.draw()
            combined_layout.addWidget(canvas)
        
        # Se envía la imágen vacía ya que se está colocando directamente en el layout
        dialog = MessageDialog(title=title, title_color=title_color, image_name=None,  parent=self.parent_widget, custom_widget=combined_widget)
        dialog.exec()
