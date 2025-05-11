from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from utils.image_utils import create_image_label

class BasePage(QWidget):
    def __init__(self, navigate_callback=None):
        super(BasePage, self).__init__()
        self.navigate_callback = navigate_callback
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(0)

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        self.text_widget = QWidget()
        self.text_layout = QVBoxLayout(self.text_widget)
        self.text_layout.setContentsMargins(30, 40, 30, 40)
        self.text_layout.setSpacing(20)

        # Los widgets derivados deben llenar este layout
        self.setup_text_content()

        # Imagen
        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)
        image_layout.setContentsMargins(0, 0, 0, 0)

        image_container = QWidget()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        # Usar la utilidad para crear la imagen
        image = create_image_label(self.get_image_path(), width=self.get_image_width(), height=self.get_image_height())
        image_container_layout.addWidget(image)

        image_layout.addWidget(image_container)

        container_layout.addWidget(self.text_widget, 5)
        container_layout.addWidget(image_widget, 4)

        main_layout.addWidget(container)

    def setup_text_content(self):
        """Método a implementar por las clases derivadas para configurar el contenido del texto"""
        pass

    def get_image_path(self):
        """Método a implementar por las clases derivadas para obtener la ruta de la imagen"""
        return "assets/images/intro/default.png"

    def get_image_width(self):
        """Método para especificar el ancho de la imagen"""
        return 200

    def get_image_height(self):
        """Método para especificar la altura de la imagen"""
        return 200

    def create_info_item(self, icon, text):
        widget = QWidget()
        widget.setObjectName("featureItem")

        layout = QHBoxLayout(widget)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setObjectName("featureIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedWidth(32)

        text_label = QLabel(text)
        text_label.setObjectName("featureText")
        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        return widget