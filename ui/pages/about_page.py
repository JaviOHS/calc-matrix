from ui.widgets.base_page import BasePage
from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

class AboutPage(BasePage):
    def __init__(self, navigate_callback=None):
        super(AboutPage, self).__init__(navigate_callback, page_key="about")
    
    def create_intro_view(self):
        # Este método es igual que el de BasePage pero con una pequeña modificación al llamar a setup_educational_content
        scroll_area = super().create_intro_view()
        
        # Acceder al widget de scroll_area y encontrar el panel de imagen
        container = scroll_area.widget()
        for i in range(container.layout().count()):
            item = container.layout().itemAt(i)
            if item and item.widget() and item.widget().objectName() == "imagePanel":
                # Limpiar el contenido actual del panel de imagen
                image_panel = item.widget()
                while image_panel.layout().count():
                    child = image_panel.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                
                # Recrear el contenido del panel de imagen
                image_layout = image_panel.layout()
                
                # Recrear la imagen
                image_container = QFrame()
                image_container_layout = QVBoxLayout(image_container)
                image_container_layout.setContentsMargins(0, 0, 0, 0)
                
                from utils.components.image_utils import create_image_label
                image = create_image_label(
                    self.get_image_path(), 
                    width=self.get_image_width(), 
                    height=self.get_image_height()
                )
                image_container_layout.addWidget(image, 0, Qt.AlignCenter)
                image_layout.addWidget(image_container)
                
                # Usar setup_educational_content con URL de GitHub e icono
                self.setup_educational_content(
                    image_layout, 
                    external_url="https://github.com/JaviOHS/calc-matrix",
                    button_icon="github.svg"
                )
                break
                
        return scroll_area