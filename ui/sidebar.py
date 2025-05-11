from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import QSize, Qt
from utils.resources import resource_path
from utils.icon_utils import colored_svg_icon
from utils.image_utils import create_image_label 

class Sidebar(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()
        self.setFixedWidth(200)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Usar la nueva función para crear el label con la imagen del logo
        logo_label = create_image_label("assets/images/app.png", width=120, height=120)
        self.layout.addWidget(logo_label)
        
        self.layout.addWidget(QLabel("""<span style='font-size:28px; font-weight:bold; color:#037df5;'>Calc<span style='color:#ff8103;'>Matrix</span></span>""", alignment=Qt.AlignCenter))
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
