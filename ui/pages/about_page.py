from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QDesktopServices
from utils.action_buttons import ActionButton
from ui.widgets.base_page import BasePage

class AboutPage(BasePage):
    def __init__(self, navigate_callback=None):
        super(AboutPage, self).__init__(navigate_callback)

    def setup_text_content(self):
        title = QLabel("Información sobre el desarrollo")
        title.setObjectName("heroTitle")
        self.text_layout.addWidget(title)

        subtitle_highlight = QLabel("De CalcMatrix 🧑‍💻")
        subtitle_highlight.setObjectName("heroHighlight")
        self.text_layout.addWidget(subtitle_highlight)

        # Información del desarrollador
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(12)

        author_info = self.create_info_item("👤", "Javier Haro Soledispa - jharos@unemi.edu.ec")
        faculty_info = self.create_info_item("🏛️", "UNEMI - Facultad de Ciencias e Ingeniería")
        career_info = self.create_info_item("🎓", "Carrera de Ingeniería de Software")
        semester_info = self.create_info_item("📚", "Sexto Semestre - Modelos matemáticos y simulación")
        teacher_info = self.create_info_item("👨‍🏫", "Ing. Isidro Morales Torres")

        info_layout.addWidget(author_info)
        info_layout.addWidget(faculty_info)
        info_layout.addWidget(career_info)
        info_layout.addWidget(semester_info)
        info_layout.addWidget(teacher_info)
        info_widget.setObjectName("infoContainer")
        info_widget.setMaximumWidth(700)
        self.text_layout.addWidget(info_widget)

        # Botón de GitHub
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)

        github_button = ActionButton("Repositorio de GitHub", icon_name="github.svg", icon_size=QSize(20, 20), object_name="ctaButton")
        github_button.clicked.connect(self.open_github)        

        button_layout.addWidget(github_button)
        button_layout.addStretch()

        self.text_layout.addWidget(button_container)
        self.text_layout.addStretch()

    def get_image_path(self):
        return "assets/images/intro/about.png"
    
    def get_image_width(self):
        return 230

    def get_image_height(self):
        return 230

    def open_github(self):
        github_url = QUrl("https://github.com/JaviOHS/calc-matrix")
        QDesktopServices.openUrl(github_url)
        