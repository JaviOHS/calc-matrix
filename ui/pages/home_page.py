from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton,QSizePolicy, QGridLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor

class MainHomePage(QWidget):
    def __init__(self, navigate_callback=None):
        super(MainHomePage, self).__init__()

        self.navigate_callback = navigate_callback

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(40)

        # Contenedor superior (título + contenido)
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(40)

        # Sección de texto a la izquierda
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(18)

        # Título como HTML
        title_label = QLabel("""
            <span style='font-size:42px; font-weight:bold; color:white;'>
                Bienvenido a <span style='color:#e74c3c;'>Calc</span><span style='color:#3498db;'>Matrix</span>!
            </span>
        """)
        title_label.setTextFormat(Qt.RichText)
        title_label.setObjectName("main_title")
        text_layout.addWidget(title_label)

        # Subtítulo como HTML
        subtitle = QLabel("""
            <span style='font-size:18px; color:#7f8c8d;'>
                Tu calculadora matemática <span style='color:#e74c3c; font-weight:bold'>inteligente</span> y 
                <span style='color:#3498db; font-weight:bold'>poderosa</span>
            </span>
        """)
        subtitle.setTextFormat(Qt.RichText)
        subtitle.setObjectName("intro_text")
        text_layout.addWidget(subtitle)

        # Texto introductorio
        intro_text = QLabel("""
            <p style='font-size:18px; color:#c0c0c0; line-height:1.6;'>
            ¡Hola, Bienvenido! 👋<br>
            Aquí puedes resolver operaciones de <span style='color:#e74c3c; font-weight:700'>matrices</span>, 
            <span style='color:#3498db; font-weight:700'>polinomios</span>, 
            <span style='color:#9b59b6; font-weight:700'>vectores</span> y mucho más.<br>
            ¡A disfrutar aprendiendo! 🚀😃
            </p>
        """)
        intro_text.setWordWrap(True)
        intro_text.setTextFormat(Qt.RichText)
        text_layout.addWidget(intro_text)

        # Botón Empezar
        start_button = QPushButton("¡Empezar ahora!")
        start_button.setObjectName("start_button")
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setFixedSize(200, 50)
        start_button.clicked.connect(self.go_to_matrix_page)
        text_layout.addWidget(start_button, alignment=Qt.AlignLeft)
        text_layout.addStretch()

        # Sección de imagen a la derecha
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(20)

        image_label = QLabel()
        pixmap = QPixmap("assets/images/intro/deco.png")
        image_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)

        # Añadir secciones al layout superior
        top_layout.addWidget(text_container, 1)
        top_layout.addWidget(image_container, 0, Qt.AlignTop)

        # Añadir contenedor superior al layout principal
        main_layout.addWidget(top_container)

    def go_to_matrix_page(self):
        self.navigate_callback("matrix")
