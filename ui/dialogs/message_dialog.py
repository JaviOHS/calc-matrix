from utils.resources import resource_path
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QSizePolicy, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from ui.widgets.action_buttons import ActionButton

class MessageDialog(QDialog):
    def __init__(self, title: str, title_color: str, message: str = "", image_name: str = "success.png", parent=None, custom_widget: QWidget = None):
        super().__init__(parent)

        # Ventana sin bordes y con fondo transparente
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self._drag_position = None

        # CONTENEDOR CON BORDES REDONDEADOS Y COLOR DE FONDO
        background_frame = QFrame(self)
        background_frame.setObjectName("backgroundFrame")
        background_layout = QVBoxLayout(background_frame)
        background_layout.setContentsMargins(20, 20, 20, 20)
        background_layout.setSpacing(20)

        # Título
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleDialog")
        title_label.setStyleSheet(f"color: {title_color};")
        background_layout.addWidget(title_label)

        # Contenido principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        if image_name:
            image_path = resource_path(f"assets/images/dialogs/{image_name}")
            pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            content_layout.addWidget(image_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        if custom_widget:
            content_layout.addWidget(custom_widget, alignment=Qt.AlignCenter)
        else:
            message_label = QLabel(message)
            message_label.setWordWrap(True)
            message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            message_label.setObjectName("messageDialog")
            message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_layout.addWidget(message_label)

        background_layout.addLayout(content_layout)

        # Botón aceptar
        button = ActionButton("Aceptar", icon_name="check.svg", icon_size=QSize(20, 20), object_name="ctaButton")
        button.clicked.connect(self.accept)
        button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        background_layout.addLayout(button_layout)

        # Layout externo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(background_frame)

        self.adjustSize()
