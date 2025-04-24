from utils.resources import resource_path
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QDesktopServices, QPixmap
from PySide6.QtCore import QUrl

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super(AboutPage, self).__init__(parent)

        # Layout principal similar al de MainHomePage
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(40)

        # Contenedor de contenido con margen y separación
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(40)

        # Texto informativo alineado a la izquierda
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(20)

        # Título principal
        title_label = QLabel("""
            <span style='font-size:38px; font-weight:bold; color:white;'>
                Acerca de <span style='color:#e74c3c;'>Calc</span><span style='color:#3498db;'>Matrix</span>
            </span>
        """)
        title_label.setTextFormat(Qt.RichText)
        text_layout.addWidget(title_label)

        # Info autor y docente
        info_label = QLabel("""
            <p style='font-size:18px; color:#c0c0c0; line-height:1.6;'>
                <b>Javier Haro Soledispa</b><br>
                Estudiante de Ingeniería de Software - 6to semestre<br><br>
                <b>Docente:</b> Ing. Fabricio Morales Torres <br><br>
                <b>Proyecto para la asignatura:</b><br>
                <i>Modelos Matemáticos y Simulación</i>
            </p>
        """)
        info_label.setTextFormat(Qt.RichText)
        info_label.setWordWrap(True)
        text_layout.addWidget(info_label)

        # Botón GitHub
        github_button = QPushButton(" Ver repositorio en GitHub")
        github_icon = QIcon(resource_path("assets/icons/github.svg"))
        github_button.setIcon(github_icon)
        github_button.setCursor(Qt.PointingHandCursor)
        github_button.setFixedSize(260, 45)
        github_button.setStyleSheet("""
            QPushButton {
                font-size: 15px;
                padding: 10px;
                color: white;
                border-radius: 8px;
            }
        """)
        github_button.clicked.connect(self.open_github_repo)
        text_layout.addWidget(github_button, alignment=Qt.AlignLeft)
        text_layout.addStretch()

        # Imagen decorativa a la derecha (opcional)
        image_label = QLabel()
        pixmap = QPixmap(resource_path("assets/images/intro/about.png"))
        image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)

        # Agregar al layout principal
        content_layout.addWidget(text_container, 1)
        content_layout.addWidget(image_label, 0, Qt.AlignTop)
        main_layout.addWidget(content_container)

    def open_github_repo(self):
        url = QUrl("https://github.com/TU_USUARIO/TU_REPOSITORIO")  # Reemplázalo con tu URL real
        QDesktopServices.openUrl(url)
