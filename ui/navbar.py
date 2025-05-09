from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt, QSize
from utils.resources import resource_path
from utils.icon_utils import colored_svg_pixmap
from ui.widgets.action_buttons import ActionButton
class TopNavbar(QWidget):
    def __init__(self, main_window, toggle_sidebar_callback, username="Usuario"):
        super().__init__()
        self.main_window = main_window
        self.setFixedHeight(50)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        # Botón de menú (icono SVG)
        self.menu_button = ActionButton("", icon_name="menu.svg", icon_size=QSize(24, 24), object_name="ctaButton")
        self.menu_button.clicked.connect(toggle_sidebar_callback)
        self.menu_button.setFixedSize(40, 40)
        layout.addWidget(self.menu_button)
        layout.addStretch()

        # Nombre del usuario
        self.username_label = QLabel(username)
        self.username_label.setFixedHeight(40)
        self.username_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.username_label)

        self.avatar = QLabel()
        self.avatar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        user_icon_path = resource_path("assets/icons/user.svg")
        colored_pixmap = colored_svg_pixmap(user_icon_path, QColor("#acadae"), QSize(32, 32))
        self.avatar.setPixmap(colored_pixmap)
        self.avatar.setFixedSize(32, 32)
        layout.addWidget(self.avatar)

        # Botón minimizar con ActionButton
        self.min_button = ActionButton("",icon_name="minimize.svg", icon_size=QSize(20, 20), object_name="minButton")
        self.min_button.setFixedSize(32, 32)
        self.min_button.clicked.connect(self.main_window.showMinimized)
        layout.addWidget(self.min_button)

        # Botón cerrar con ActionButton
        self.close_button = ActionButton("", icon_name="close.svg", icon_size=QSize(20, 20),object_name="closeButton")
        self.close_button.setFixedSize(32, 32)
        self.close_button.clicked.connect(self.main_window.close)
        layout.addWidget(self.close_button)
