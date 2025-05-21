from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from utils.components.action_buttons import ActionButton
from utils.components.image_utils import create_image_label

class EducationalContentManager:
    @staticmethod
    def create_educational_card(title, fact, image_path, image_width=180, image_height=120):
        """Crea una tarjeta educativa con título, texto e imagen"""
        edu_card = QFrame()
        edu_card.setObjectName("educationalCard")
        edu_layout = QVBoxLayout(edu_card)
        
        # Título educativo
        edu_title = QLabel(title)
        edu_title.setObjectName("eduTitle")
        edu_title.setWordWrap(True)
        edu_layout.addWidget(edu_title)
        
        # Texto educativo
        edu_fact = QLabel(fact)
        edu_fact.setObjectName("eduFact")
        edu_fact.setWordWrap(True)
        edu_layout.addWidget(edu_fact)

        # Imagen educativa
        edu_image = create_image_label(image_path, width=image_width, height=image_height)
        edu_image.setAlignment(Qt.AlignCenter)
        edu_image.setObjectName("eduImage")
        edu_layout.addWidget(edu_image, 0, Qt.AlignCenter)
        
        edu_layout.addSpacing(10)
        
        return edu_card

    @staticmethod
    def create_cta_container(text, button_text, footer_text="", button_icon=None):
        """Crea un contenedor de Call-to-Action"""
        cta_container = QFrame()
        cta_container.setObjectName("ctaContainer")
        cta_layout = QVBoxLayout(cta_container)
        cta_layout.setContentsMargins(15, 0, 15, 15)
        
        # Texto CTA
        cta_text = QLabel(text)
        cta_text.setObjectName("ctaText")
        cta_text.setWordWrap(True)
        cta_layout.addWidget(cta_text)
        
        # Botón
        button_row = QFrame()
        button_layout = QHBoxLayout(button_row)
        button_layout.setContentsMargins(0, 12, 0, 0)
        
        if button_icon:
            start_button = ActionButton.custom_icon(button_text, button_icon)
        else:
            start_button = ActionButton.primary(button_text)
        
        button_layout.addWidget(start_button)
        button_layout.addStretch()
        cta_layout.addWidget(button_row)
        
        # Footer
        if footer_text:
            footer = QLabel(footer_text)
            footer.setObjectName("footerText")
            footer.setWordWrap(True)
            cta_layout.addWidget(footer)
        
        return cta_container, start_button

    @staticmethod
    def setup_educational_content(parent_widget, content_data, layout, button_callback=None, external_url=None, button_icon=None):
        """Configura todo el contenido educativo incluyendo CTA y tarjeta educativa"""
        
        # Crear CTA
        cta_text = content_data.get("cta", {}).get("text", "¿Listo para empezar?")
        button_text = content_data.get("cta", {}).get("button", "Comenzar")
        footer_text = content_data.get("cta", {}).get("footer", "")
        
        cta_container, start_button = EducationalContentManager.create_cta_container(
            cta_text, 
            button_text, 
            footer_text,
            button_icon
        )
        
        # Configurar callback del botón
        if external_url:
            start_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(external_url)))
        elif button_callback:
            start_button.clicked.connect(button_callback)
        
        layout.addWidget(cta_container)
        
        layout.addSpacing(20) 
        
        # Crear tarjeta educativa si existe el contenido
        if "educational" in content_data:
            edu_data = content_data["educational"]
            edu_card = EducationalContentManager.create_educational_card(
                edu_data.get("title", "¿Sabías que...?"),
                edu_data.get("fact", ""),
                "assets/images/educational.png"
            )
            layout.addWidget(edu_card)
        
        return start_button

    @staticmethod
    def get_educational_content(content_data):
        """Obtiene el contenido educativo del JSON"""
        return {
            "title": content_data.get("educational", {}).get("title", "¿Sabías que...?"),
            "fact": content_data.get("educational", {}).get("fact", ""),
            "image": content_data.get("educational", {}).get("image", "assets/images/educational.png")
        }

    @staticmethod
    def get_cta_content(content_data):
        """Obtiene el contenido CTA del JSON"""
        return {
            "text": content_data.get("cta", {}).get("text", "¿Listo para empezar?"),
            "button": content_data.get("cta", {}).get("button", "Comenzar"),
            "footer": content_data.get("cta", {}).get("footer", "")
        }