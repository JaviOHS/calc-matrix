from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
from PySide6.QtCore import Qt
from ui.widgets.base_page import BasePage
from utils.image_utils import create_image_label

class MainHomePage(BasePage):
    def __init__(self, navigate_callback=None):
        super(MainHomePage, self).__init__(navigate_callback, page_key="home")
        
    def go_to_first_page(self):
        target = self.page_content.get("cta", {}).get("target", "matrix")
        self.navigate_callback(target)

    def create_intro_view(self):
        # Crear un área de desplazamiento para contenido largo
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        container = QFrame()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        # Panel de contenido principal
        self.text_panel = QFrame()
        self.text_panel.setObjectName("contentPanel")
        self.text_layout = QVBoxLayout(self.text_panel)
        self.text_layout.setSpacing(24)
        self.text_layout.setContentsMargins(28, 28, 28, 28)

        self.setup_text_content() # Los widgets derivados deben llenar este layout

        # Imagen con efectos visuales mejorados
        image_panel = QFrame()
        image_panel.setObjectName("imagePanel")
        image_layout = QVBoxLayout(image_panel)
        # Reducir el margen inferior para que el CTA esté más cerca
        image_layout.setContentsMargins(20, 20, 20, 0)

        image_container = QFrame()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        # Usar la utilidad para crear la imagen
        image = create_image_label(self.get_image_path(), width=self.get_image_width(), height=self.get_image_height())
        image_container_layout.addWidget(image, 0, Qt.AlignCenter)

        image_layout.addWidget(image_container)
        
        # Agregar contenido educativo adicional con nuestro callback personalizado
        self.setup_educational_content(image_layout, self.go_to_first_page)

        container_layout.addWidget(self.text_panel, stretch=6)
        container_layout.addWidget(image_panel, stretch=4)

        scroll_area.setWidget(container)
        return scroll_area
