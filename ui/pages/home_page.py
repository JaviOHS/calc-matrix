from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from utils.action_buttons import ActionButton
from ui.widgets.base_page import BasePage

class MainHomePage(BasePage):
    def __init__(self, navigate_callback=None):
        super(MainHomePage, self).__init__(navigate_callback)

    def setup_text_content(self):
        title = QLabel("Domina las Matemáticas")
        title.setObjectName("heroTitle")
        self.text_layout.addWidget(title)

        subtitle_highlight = QLabel("Con CalcMatrix 🧑‍💻")
        subtitle_highlight.setObjectName("heroHighlight")
        self.text_layout.addWidget(subtitle_highlight)

        description = QLabel("""
        👋 ¡Bienvenido a CalcMatrix! Tu solución para problemas matemáticos avanzados. 
        ✨ Explora matrices, sistemas de ecuaciones y polinomios en un entorno intuitivo y potente.
        """)
        description.setObjectName("heroDescription")
        description.setWordWrap(True)
        self.text_layout.addWidget(description)

        # Features
        features = QWidget()
        features.setObjectName("featureContainer")
        features_layout = QVBoxLayout(features)
        features_layout.setSpacing(12)

        feature1 = self.create_info_item("📊", "Operaciones con matrices completas")
        feature2 = self.create_info_item("🧮", "Resolución de operaciones simbólicas")
        feature3 = self.create_info_item("📈", "Análisis de polinomios avanzado")

        features_layout.addWidget(feature1)
        features_layout.addWidget(feature2)
        features_layout.addWidget(feature3)

        features.setMaximumWidth(400)
        self.text_layout.addWidget(features)

        # Botón y texto
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)

        button = ActionButton.primary("Comenzar ahora")
        button.clicked.connect(self.go_to_first_page)

        footer_text = QLabel("🙋 Dale una oportunidad a nuestro sistema y sé parte de nuestra comunidad.")
        footer_text.setObjectName("footerText")

        button_layout.addWidget(button)
        button_layout.addWidget(footer_text)
        button_layout.addStretch()

        self.text_layout.addWidget(button_container)
        self.text_layout.addStretch()

    def get_image_path(self):
        return "assets/images/intro/deco.png"
        
    def get_image_width(self):
        return 192
        
    def get_image_height(self):
        return 192

    def go_to_first_page(self):
        self.navigate_callback("matrix")
