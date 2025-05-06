from utils.resources import resource_path
from utils.icon_utils import colored_svg_icon
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QDesktopServices, QPixmap, QColor

class AboutPage(QWidget):
    def __init__(self, navigate_callback=None):
        super(AboutPage, self).__init__()
        self.navigate_callback = navigate_callback
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(0)

        container = QWidget()
        container.setObjectName("mainContainer")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        text_widget = QWidget()
        text_widget.setObjectName("textSection")
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(30, 40, 30, 40)
        text_layout.setSpacing(20)

        title = QLabel("Información sobre el desarrollo")
        title.setObjectName("heroTitle")
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: white;")
        text_layout.addWidget(title)

        subtitle_highlight = QLabel("De CalcMatrix 🧑‍💻")
        subtitle_highlight.setObjectName("heroHighlight")
        subtitle_highlight.setStyleSheet("font-size: 24px; font-weight: bold; color: #ff8103;")
        text_layout.addWidget(subtitle_highlight)

        # Información del desarrollador
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(12)

        author_info = self.create_info_item("👤", "Javier Haro Soledispa - jharos@unemi.edu.ec")
        faculty_info = self.create_info_item("🏛️", "Facultad de Ciencias e Ingeniería")
        career_info = self.create_info_item("🎓", "Carrera de Ingeniería de Software")
        semester_info = self.create_info_item("📚", "Sexto Semestre - Modelos matemáticos y simulación")
        teacher_info = self.create_info_item("👨‍🏫", "Ing. Isidro Morales Torres")

        info_layout.addWidget(author_info)
        info_layout.addWidget(faculty_info)
        info_layout.addWidget(career_info)
        info_layout.addWidget(semester_info)
        info_layout.addWidget(teacher_info)

        info_widget.setStyleSheet("background-color: #1f2b3d; border-radius: 10px; padding: 20px;")
        info_widget.setMaximumWidth(500)
        text_layout.addWidget(info_widget)

        # Botón de GitHub
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)

        github_button = QPushButton("Repositorio GitHub")
        github_button.setObjectName("ctaButton")
        github_button.setCursor(Qt.PointingHandCursor)
        icon_path = resource_path("assets/icons/github.svg")
        icon = colored_svg_icon(icon_path, QColor(28, 44, 66))
        github_button.setIcon(icon)
        github_button.setIconSize(QSize(20, 20))
        github_button.clicked.connect(self.open_github)

        button_layout.addWidget(github_button)
        button_layout.addStretch()

        text_layout.addWidget(button_container)
        text_layout.addStretch()

        # Imagen (puedes cambiarla por una relevante)
        image_widget = QWidget()
        image_widget.setObjectName("imageSection")
        image_layout = QVBoxLayout(image_widget)
        image_layout.setContentsMargins(0, 0, 0, 0)

        image_container = QWidget()
        image_container.setObjectName("imageContainer")
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        image = QLabel()
        pixmap = QPixmap(resource_path("assets/images/intro/about.png"))  # Puedes cambiar esta imagen
        image.setPixmap(pixmap.scaled(230, 230, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        image_container_layout.addWidget(image)

        image_layout.addWidget(image_container)

        container_layout.addWidget(text_widget, 5)
        container_layout.addWidget(image_widget, 4)

        main_layout.addWidget(container)

    def create_info_item(self, icon, text):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setObjectName("featureIcon")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px; color: #ff8103;")
        icon_label.setFixedWidth(32)

        text_label = QLabel(text)
        text_label.setObjectName("featureText")
        text_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: 500;
            padding-left: 6px;
            border-left: 2px solid #ff8103;
        """)
        text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        widget.setStyleSheet("""
            background-color: #2e3b4e;
            border-radius: 6px;
            padding: 6px;
        """)

        return widget

    def open_github(self):
        github_url = QUrl("https://github.com/JaviOHS/calc-matrix")
        QDesktopServices.openUrl(github_url)
