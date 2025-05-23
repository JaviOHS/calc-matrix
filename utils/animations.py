from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QPoint, QEasingCurve
from PySide6.QtWidgets import QWidget

class PageAnimations:
    # Constantes de dirección
    LEFT_TO_RIGHT = QPoint(-20, 0)  # El widget aparece desde la izquierda
    RIGHT_TO_LEFT = QPoint(20, 0)   # El widget aparece desde la derecha
    TOP_TO_BOTTOM = QPoint(0, -20)  # El widget aparece desde arriba
    BOTTOM_TO_TOP = QPoint(0, 20)   # El widget aparece desde abajo
    
    # Constantes de duración
    DURATION_FAST = 300    # Para transiciones rápidas
    DURATION_NORMAL = 400  # Para transiciones estándar
    DURATION_SLOW = 600    # Para transiciones más suaves
    
    # Nuevas constantes para diálogos
    SCALE_NORMAL = 1.0
    SCALE_SMALL = 0.8
    
    @staticmethod
    def fade_slide_in(widget: QWidget, duration: int = DURATION_NORMAL, direction: QPoint = RIGHT_TO_LEFT) -> QParallelAnimationGroup:
        """Crea una animación combinada de fundido y deslizamiento
        
        Args:
            widget: Widget a animar
            duration: Duración de la animación en milisegundos
            direction: Dirección de la animación. Usar las constantes definidas:
                      LEFT_TO_RIGHT: Widget entra desde la izquierda
                      RIGHT_TO_LEFT: Widget entra desde la derecha (default)
                      TOP_TO_BOTTOM: Widget entra desde arriba
                      BOTTOM_TO_TOP: Widget entra desde abajo
        """
        animation_group = QParallelAnimationGroup()
        
        # Animación de posición
        slide = QPropertyAnimation(widget, b"pos")
        start_pos = widget.pos() - direction
        slide.setStartValue(start_pos)
        slide.setEndValue(widget.pos())
        slide.setDuration(duration)
        slide.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animación de opacidad
        fade = QPropertyAnimation(widget, b"windowOpacity")
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setDuration(duration)
        fade.setEasingCurve(QEasingCurve.OutCubic)
        
        # Agregar ambas animaciones al grupo
        animation_group.addAnimation(slide)
        animation_group.addAnimation(fade)
        return animation_group
    
    @staticmethod
    def fade_scale_in(widget, duration: int = DURATION_NORMAL):
        """Crea una animación combinada de fundido y escala para diálogos
        
        Args:
            widget: Widget a animar
            duration: Duración de la animación en milisegundos
        """
        animation_group = QParallelAnimationGroup()
        
        # Animación de opacidad
        fade = QPropertyAnimation(widget, b"windowOpacity")
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setDuration(duration)
        fade.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animación de escala
        scale = QPropertyAnimation(widget, b"geometry")
        initial_geometry = widget.geometry()
        scaled_geometry = initial_geometry
        scaled_geometry.setSize(initial_geometry.size() * PageAnimations.SCALE_SMALL)
        scaled_geometry.moveCenter(initial_geometry.center())
        
        scale.setStartValue(scaled_geometry)
        scale.setEndValue(initial_geometry)
        scale.setDuration(duration)
        scale.setEasingCurve(QEasingCurve.OutBack)
        
        animation_group.addAnimation(fade)
        animation_group.addAnimation(scale)
        return animation_group
