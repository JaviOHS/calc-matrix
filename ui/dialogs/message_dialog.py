from ui.dialogs.base_dialog import BaseDialog
from PySide6.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt
from utils.components.image_utils import create_image_label

class MessageDialog(BaseDialog):
    def __init__(self, title: str, title_color: str, message: str = "", image_name: str = "success.png", parent=None, custom_widget: QWidget = None):
        self.message = message
        self.image_name = image_name
        self.custom_widget = custom_widget
        super().__init__(title, title_color, parent)
        self.finalize()

    def setup_content_area(self):
        # Contenido principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Usar la utilidad para crear la imagen
        if self.image_name:
            image_path = f"assets/images/dialogs/{self.image_name}"
            image_label = create_image_label(image_path, width=150, height=150)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            content_layout.addWidget(image_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        if self.custom_widget:
            content_layout.addWidget(self.custom_widget, alignment=Qt.AlignCenter)
        else:
            message_label = QLabel(self.message)
            message_label.setWordWrap(True)
            message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            message_label.setObjectName("messageDialog")
            message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_layout.addWidget(message_label)

        self.background_layout.addLayout(content_layout)
        