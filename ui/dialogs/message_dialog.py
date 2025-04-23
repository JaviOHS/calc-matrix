from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class MessageDialog(QDialog):
    def __init__(self, title: str, message: str = "", image_name: str = "success.png", parent=None, custom_widget: QWidget = None):
        super().__init__(parent)

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self._drag_position = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 20px;")
        main_layout.addWidget(title_label)

        # Contenedor horizontal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Imagen (izquierda)
        if image_name:
            image_path = os.path.join("assets", "images", "dialogs", image_name)
            pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            content_layout.addWidget(image_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Widget o mensaje (derecha)
        if custom_widget:
            content_layout.addWidget(custom_widget, alignment=Qt.AlignCenter)
        else:
            message_label = QLabel(message)
            message_label.setWordWrap(True)
            message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            message_label.setStyleSheet("font-size: 18px;")
            message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_layout.addWidget(message_label)

        main_layout.addLayout(content_layout)

        # Botón cerrar
        button = QPushButton("Aceptar")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.accept)
        button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.adjustSize()