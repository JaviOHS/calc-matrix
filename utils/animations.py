from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget

class PageAnimations:
    # Constantes de dirección
    LEFT_TO_RIGHT = QPoint(-50, 0)
    RIGHT_TO_LEFT = QPoint(50, 0)
    TOP_TO_BOTTOM = QPoint(0, -50)
    BOTTOM_TO_TOP = QPoint(0, 50)
    
    # Duraciones
    DURATION_FAST = 200
    DURATION_NORMAL = 300
    DURATION_SLOW = 400

    @staticmethod
    def fade_slide_in(widget: QWidget, duration: int = 300, direction: QPoint = LEFT_TO_RIGHT) -> QParallelAnimationGroup:
        """
        Crea una animación combinada de fade y slide con efecto easing
        """
        # Grupo de animaciones paralelas
        animation_group = QParallelAnimationGroup()

        # Animación de opacidad
        fade_animation = QPropertyAnimation(widget, b"windowOpacity")
        fade_animation.setStartValue(0.0)
        fade_animation.setEndValue(1.0)
        fade_animation.setDuration(duration)
        fade_animation.setEasingCurve(QEasingCurve.OutCubic)

        # Animación de posición
        pos_animation = QPropertyAnimation(widget, b"pos")
        start_pos = widget.pos() + direction
        end_pos = widget.pos()
        
        pos_animation.setStartValue(start_pos)
        pos_animation.setEndValue(end_pos)
        pos_animation.setDuration(duration)
        pos_animation.setEasingCurve(QEasingCurve.OutCubic)

        # Agregar animaciones al grupo
        animation_group.addAnimation(fade_animation)
        animation_group.addAnimation(pos_animation)

        return animation_group
 