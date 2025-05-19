from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QSize
from utils.components.action_buttons import ActionButton

class BaseDialog(QDialog):
    """Clase base para todos los diálogos de la aplicación"""
    def __init__(self, title="", title_color=None, parent=None):
        super().__init__(parent)

        # Ventana sin bordes y con fondo transparente
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self._drag_position = None

        # Contenedor con borde redondeado
        self.background_frame = QFrame(self)
        self.background_frame.setObjectName("backgroundFrame")
        self.background_layout = QVBoxLayout(self.background_frame)
        self.background_layout.setContentsMargins(20, 20, 20, 20)
        self.background_layout.setSpacing(20)

        # Título
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("titleDialog")
        if title_color:
            self.title_label.setStyleSheet(f"color: {title_color};")
        self.background_layout.addWidget(self.title_label)

        # Contenedor principal (a implementar en subclases)
        self.setup_content_area()

        # Botón aceptar
        self.setup_button_area()

        # Layout externo
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.background_frame)

    def setup_content_area(self):
        """Método para implementar en subclases"""
        pass

    def setup_button_area(self):
        """Configura el área de botones"""
        button = ActionButton("Aceptar", icon_name="check.svg", icon_size=QSize(20, 20), object_name="ctaButton")
        button.clicked.connect(self.accept)
        button.setFixedWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        self.background_layout.addLayout(button_layout)

    def finalize(self):
        """Finaliza la configuración del diálogo y ajusta su tamaño"""
        self.adjustSize()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_position is not None:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
            