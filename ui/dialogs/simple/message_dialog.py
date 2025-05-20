from ui.dialogs.base.base_dialog import BaseDialog
from PySide6.QtWidgets import QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from utils.components.image_utils import create_image_label

class MessageDialog(BaseDialog):
    """Diálogo para mostrar mensajes con una imagen opcional"""
    def __init__(self, title="", title_color=None, message="", image_name=None, parent=None, custom_widget=None):
        self.message = message
        self.image_name = image_name
        self.custom_widget = custom_widget
        super().__init__(title, title_color, parent)
        self.finalize()

    def setup_content_area(self):
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Añadir imagen si está especificada
        if self.image_name:
            self._add_image(content_layout)

        # Añadir contenido personalizado o mensaje
        if self.custom_widget:
            content_layout.addWidget(self.custom_widget, alignment=Qt.AlignCenter)
        else:
            self._add_message_label(content_layout)

        self.background_layout.addLayout(content_layout)
    
    def _add_image(self, layout):
        """Añade la imagen al layout"""
        image_path = f"assets/images/dialogs/{self.image_name}"
        image_label = create_image_label(image_path, width=150, height=150)
        image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(image_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)
    
    def _add_message_label(self, layout):
        """Añade el label del mensaje al layout"""
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        message_label.setObjectName("messageDialog")
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(message_label)