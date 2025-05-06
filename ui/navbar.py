from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from utils.resources import resource_path
from utils.icon_utils import colored_svg_icon

class TopNavbar(QWidget):
    def __init__(self, main_window, toggle_sidebar_callback, username="Usuario"):
        super().__init__()
        self.main_window = main_window
        self.setFixedHeight(50)
        self.setObjectName("navbar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Botón de menú (icono SVG)
        self.menu_button = QPushButton()
        self.menu_button.setObjectName("ctaButton")
        icon_path = resource_path("assets/icons/menu.svg")
        icon = colored_svg_icon(icon_path, QColor(28, 44, 66))
        self.menu_button.setIcon(QIcon(icon))
        self.menu_button.setIconSize(QSize(24, 24))
        self.menu_button.setCursor(Qt.PointingHandCursor)
        self.menu_button.clicked.connect(toggle_sidebar_callback)
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
        user_icon_path = resource_path("assets/icons/user.svg")
        pixmap = QPixmap(user_icon_path)
        self.avatar.setPixmap(pixmap.scaled(36, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.avatar.setFixedSize(36, 36)
        self.avatar.setProperty("class", "navbar-avatar")
        layout.addWidget(self.avatar)

        # Botón minimizar (SVG)
        self.min_button = QPushButton()
        min_icon_path = resource_path("assets/icons/minimize.svg")
        self.min_button.setIcon(QIcon(min_icon_path))
        self.min_button.setIconSize(QSize(20, 20))
        self.min_button.setFixedSize(36, 36)
        self.min_button.setCursor(Qt.PointingHandCursor)
        self.min_button.clicked.connect(self.main_window.showMinimized)
        self.min_button.setStyleSheet("""
            QPushButton {
                background-color: #10a4fc;
                border: none;
            }
            QPushButton:hover {
                background-color: #1f97df;
            }
        """)
        layout.addWidget(self.min_button)

        # Botón cerrar (SVG)
        self.close_button = QPushButton()
        close_icon_path = resource_path("assets/icons/close.svg")
        self.close_button.setIcon(QIcon(close_icon_path))
        self.close_button.setIconSize(QSize(20, 20))
        self.close_button.setFixedSize(36, 36)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.main_window.close)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #e81123;
                border: none;
            }
            QPushButton:hover {
                background-color: #c50f1f;
            }
        """)
        layout.addWidget(self.close_button)
