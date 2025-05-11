from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QSizePolicy, QFrame
from PySide6.QtCore import Qt, QSize
from utils.action_buttons import ActionButton
from utils.image_utils import create_image_label

class MessageDialog(QDialog):
    def __init__(self, title: str, title_color: str, message: str = "", image_name: str = "success.png", parent=None, custom_widget: QWidget = None):
        super().__init__(parent)

        # Ventana sin bordes y con fondo transparente
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self._drag_position = None

        # Contenedor con borde redondeado y fondo
        background_frame = QFrame(self)
        background_frame.setObjectName("backgroundFrame")
        background_layout = QVBoxLayout(background_frame)
        background_layout.setContentsMargins(20, 20, 20, 20)
        background_layout.setSpacing(20)

        # Título
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("titleDialog")
        title_label.setStyleSheet(f"color: {title_color};")
        background_layout.addWidget(title_label)

        # Contenido principal
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)

        # Usar la utilidad para crear la imagen
        if image_name:
            image_path = f"assets/images/dialogs/{image_name}"
            
            # Crear el QLabel con la imagen ya configurada
            image_label = create_image_label(image_path, width=150, height=150)
            
            # Configurar política de tamaño para que no se expanda
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            # Añadir al layout
            content_layout.addWidget(image_label, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        if custom_widget:
            content_layout.addWidget(custom_widget, alignment=Qt.AlignCenter)
        else:
            message_label = QLabel(message)
            message_label.setWordWrap(True)
            message_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            message_label.setObjectName("messageDialog")
            message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            content_layout.addWidget(message_label)

        background_layout.addLayout(content_layout)

        # Botón aceptar
        button = ActionButton("Aceptar", icon_name="check.svg", icon_size=QSize(20, 20), object_name="ctaButton")
        button.clicked.connect(self.accept)
        button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        background_layout.addLayout(button_layout)

        # Layout externo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(background_frame)

        self.adjustSize()
