from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import QSize, Qt
from utils.resources import resource_path
from utils.icon_utils import colored_svg_icon

class Sidebar(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.setFixedWidth(200)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        logo_label = QLabel()
        image_path = resource_path("assets/icons/app.png")
        pixmap = QPixmap(image_path)
        logo_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label)

        name_label = QLabel("""
            <span style='font-size:28px; font-weight:bold; color:#037df5;'>
                Calc<span style='color:#ff8103;'>Matrix</span>
            </span>
        """)
        name_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(name_label)
        self.layout.addSpacing(10)

        self.buttons = {}
        self.active_button = None

        items = {
            "Inicio": "home",
            "Matrices": "matrix",
            "Polinomios": "polynomial",
            "Vectores": "vector",
            "Gráficas": "graph",
            "C. Simbólico": "sym_cal",
            "Acerca de": "about",
        }

        for name, key in items.items():
            btn = QPushButton(name)
            btn.setProperty("class", "sidebar-button")
            btn.setProperty("active", False)

            icon_path = resource_path(f"assets/icons/{key.lower()}.svg")
            icon = colored_svg_icon(icon_path, QColor(154, 154, 155))
            btn.setIcon(icon)
            btn.setIconSize(QSize(24, 24))
            btn.setCursor(Qt.PointingHandCursor)
            self.layout.addWidget(btn)

            # Guardamos tanto el botón como el path del ícono
            self.buttons[key] = {
                "button": btn,
                "icon_path": icon_path
            }

            btn.clicked.connect(lambda _, k=key: self.on_button_clicked(k, switch_page_callback))

        self.layout.addStretch()
        self.set_active_button("home")

    def on_button_clicked(self, key, callback):
        self.set_active_button(key)
        callback(key)

    def set_active_button(self, key):
        for k, data in self.buttons.items():
            btn = data["button"]
            icon_path = data["icon_path"]
            is_active = (k == key)

            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

            color = QColor(28, 44, 66) if is_active else QColor(154, 154, 155)
            btn.setIcon(colored_svg_icon(icon_path, color))
