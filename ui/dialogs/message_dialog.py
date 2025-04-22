from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class MessageDialog(QDialog):
    def __init__(self, title: str, message: str, image_name: str, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self._drag_position = None

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Título centrado
        title_label = QLabel(title)
        title_label.setObjectName("TitleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; margin-bottom: 15px;")
        main_layout.addWidget(title_label)

        # Contenedor horizontal: imagen + mensaje
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Cargar imagen (a la izquierda)
        image_path = os.path.join("assets", "images", "dialogs", image_name)
        pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        content_layout.addWidget(image_label, alignment=Qt.AlignLeft | Qt.AlignTop)

        # Mensaje (a la derecha)
        message_label = QLabel(message)
        message_label.setObjectName("MessageLabel")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        message_label.setStyleSheet("font-size: 18px;")
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        content_layout.addWidget(message_label)

        main_layout.addLayout(content_layout)

        # Botón de aceptar centrado
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._drag_position:
            delta = event.globalPosition().toPoint() - self._drag_position
            self.move(self.pos() + delta)
            self._drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._drag_position = None
        