from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from utils.resources import resource_path

class TopNavbar(QWidget):
    def __init__(self, toggle_sidebar_callback, username="Usuario"):
        super().__init__()
        self.setFixedHeight(50)
        self.setObjectName("navbar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Botón de menú (icono SVG)
        self.menu_button = QPushButton()
        icon_path = resource_path("assets/icons/menu.svg")
        self.menu_button.setIcon(QIcon(icon_path))
        self.menu_button.setIconSize(QSize(24, 24))
        self.menu_button.setCursor(Qt.PointingHandCursor)
        self.menu_button.clicked.connect(toggle_sidebar_callback)
        self.menu_button.setProperty("class", "menu-button")
        self.menu_button.setFixedSize(40, 40)
        layout.addWidget(self.menu_button)
        layout.addStretch()

        # Nombre del usuario
        self.username_label = QLabel(username)
        self.username_label.setProperty("class", "navbar-username")
        self.username_label.setFixedHeight(40)
        self.username_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.username_label)

        # Avatar
        self.avatar = QLabel()
        pixmap = QPixmap("assets/icons/user.svg")
        self.avatar.setPixmap(pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.avatar.setFixedSize(36, 36)
        self.avatar.setProperty("class", "navbar-avatar")
        layout.addWidget(self.avatar)
    