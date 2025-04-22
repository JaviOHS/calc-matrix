from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt

class Sidebar(QWidget):
    def __init__(self, switch_page_callback):
        super().__init__()

        # Configuración de la barra lateral 
        self.setFixedWidth(200)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)  # Margenes de Sidebar

        # Logo e ícono 
        logo_label = QLabel()
        pixmap = QPixmap("assets/icons/app.png")
        logo_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label)

        # Nombre de la aplicación 
        name_label = QLabel("CalcMatrix")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setProperty("class", "sidebar-title")
        self.layout.addWidget(name_label)

        # Espacio entre encabezado y botones 
        self.layout.addSpacing(10)

        # Para botones activos
        self.buttons = {}
        self.active_button = None

        # Botones de la barra lateral 
        items = {
            "Inicio": "home",
            "Matrices": "matrix",
            "Polinomios": "polynomial",
            "Vectores": "vector",
            "Gráficas": "graph",
            "C. Simbólico": "sym_cal",
            "Acerca de": "about",
        }

        # Estilo de botones 
        for name, key in items.items():
            btn = QPushButton(name)
            btn.setProperty("class", "sidebar-button")
            btn.setProperty("active", False)  # Importante
            icon = QIcon(f"assets/icons/{key.lower()}.svg")
            btn.setIcon(icon)
            btn.setIconSize(QSize(24, 24))
            btn.setCursor(Qt.PointingHandCursor)
            self.layout.addWidget(btn)
            self.buttons[key] = btn
            btn.clicked.connect(lambda _, k=key: self.on_button_clicked(k, switch_page_callback))

        self.layout.addStretch()
        self.set_active_button("home")

    def on_button_clicked(self, key, callback):
        self.set_active_button(key)
        callback(key)

    def set_active_button(self, key):
        for k, btn in self.buttons.items():
            is_active = (k == key)
            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
            