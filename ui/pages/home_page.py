from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils.resources import resource_path
from ui.widgets.action_buttons import ActionButton

class MainHomePage(QWidget):
    def __init__(self, navigate_callback=None):
        super(MainHomePage, self).__init__()
        self.navigate_callback = navigate_callback
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(0)

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(30, 40, 30, 40)
        text_layout.setSpacing(20)

        title = QLabel("Domina las Matemáticas")
        title.setObjectName("heroTitle")
        text_layout.addWidget(title)

        subtitle_highlight = QLabel("Con CalcMatrix 🧑‍💻")
        subtitle_highlight.setObjectName("heroHighlight")
        text_layout.addWidget(subtitle_highlight)

        description = QLabel("""
        👋 ¡Bienvenido a CalcMatrix! Tu solución para problemas matemáticos avanzados. 
        ✨ Explora matrices, sistemas de ecuaciones y polinomios en un entorno intuitivo y potente.
        """)
        description.setObjectName("heroDescription")
        description.setWordWrap(True)
        text_layout.addWidget(description)

        # Features
        features = QWidget()
        features.setObjectName("featureContainer")
        features_layout = QVBoxLayout(features)
        features_layout.setSpacing(12)

        feature1 = self.create_feature("📊", "Operaciones con matrices completas")
        feature2 = self.create_feature("🧮", "Resolución de operaciones simbólicas")
        feature3 = self.create_feature("📈", "Análisis de polinomios avanzado")

        features_layout.addWidget(feature1)
        features_layout.addWidget(feature2)
        features_layout.addWidget(feature3)

        # Limitar el ancho máximo
        features.setMaximumWidth(400)  # <--- LÍNEA CLAVE

        text_layout.addWidget(features)

        # Botón y texto
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)

        button = ActionButton.primary("Comenzar ahora")
        button.clicked.connect(self.go_to_matrix_page)

        footer_text = QLabel("🙋 Dale una oportunidad a nuestro sistema y sé parte de nuestra comunidad.")
        footer_text.setObjectName("footerText")

        button_layout.addWidget(button)
        button_layout.addWidget(footer_text)
        button_layout.addStretch()

        text_layout.addWidget(button_container)
        text_layout.addStretch()

        # Imagen
        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)
        image_layout.setContentsMargins(0, 0, 0, 0)

        image_container = QWidget()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        image = QLabel()
        pixmap = QPixmap(resource_path("assets/images/intro/deco.png"))
        image.setPixmap(pixmap.scaled(192, 192, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        image_container_layout.addWidget(image)

        image_layout.addWidget(image_container)

        container_layout.addWidget(text_widget, 5)
        container_layout.addWidget(image_widget, 4)

        main_layout.addWidget(container)

    def create_feature(self, icon, text):
        widget = QWidget()
        widget.setObjectName("featureItem")

        layout = QHBoxLayout(widget)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setObjectName("featureIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedWidth(32)  # <- Ajuste clave para alinear

        text_label = QLabel(text)
        text_label.setObjectName("featureText")
        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        return widget

    def go_to_matrix_page(self):
        self.navigate_callback("matrix")
