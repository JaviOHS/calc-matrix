from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGraphicsBlurEffect
from PySide6.QtCore import Qt, QSize
from utils.components.action_buttons import ActionButton
from utils.animations import PageAnimations

class BaseDialog(QDialog):
    """Clase base para todos los diálogos de la aplicación"""
    def __init__(self, title="", title_color=None, parent=None):
        super().__init__(parent)
        self.setWindowOpacity(0.0)  # Empezar invisible para la animación

        # Variables para animaciones y efectos
        self.blur_effect = None
        self.exit_animation = None

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

    def showEvent(self, event):
        """Sobrescribe el evento show para iniciar la animación y centrar el diálogo"""
        super().showEvent(event)
        
        # Aplicar efecto de desenfoque a la ventana principal completa
        if self.parent():
            # Buscar la ventana principal (MainWindow)
            main_window = self.parent()
            while main_window.parent() is not None:
                main_window = main_window.parent()
            
            self.blur_effect = QGraphicsBlurEffect()
            self.blur_effect.setBlurRadius(10)
            main_window.setGraphicsEffect(self.blur_effect)

        # Centrar el diálogo en la pantalla DESPUÉS del showEvent
        screen = self.screen()
        center = screen.availableGeometry().center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
        # Crear la animación con la posición centrada correcta
        self.animation = PageAnimations.fade_slide_in(
            self,
            duration=PageAnimations.DURATION_NORMAL,
            direction=PageAnimations.BOTTOM_TO_TOP
        )
        self.animation.finished.connect(lambda: self.setWindowOpacity(1.0))
        
        # Iniciar la animación
        self.animation.start()

    def _remove_blur_effect(self):
        """Método auxiliar para remover el efecto de blur"""
        if self.parent() and self.blur_effect:
            # Buscar la ventana principal
            main_window = self.parent()
            while main_window.parent() is not None:
                main_window = main_window.parent()
            
            main_window.setGraphicsEffect(None)
            if hasattr(self, 'original_opacity'):
                main_window.setWindowOpacity(self.original_opacity)

    def closeEvent(self, event):
        """Remueve el efecto de desenfoque al cerrar el diálogo"""
        self._remove_blur_effect()
        super().closeEvent(event)

    def reject(self):
        """Remueve el efecto de desenfoque al rechazar el diálogo"""
        self._remove_blur_effect()
        super().reject()

    def accept(self):
        """Remueve el efecto de desenfoque al aceptar el diálogo"""
        self._remove_blur_effect()
        super().accept()

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
