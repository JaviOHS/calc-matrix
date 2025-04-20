from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtWidgets import QGraphicsOpacityEffect

def slide_to_widget(stacked_widget, new_widget, direction='left', duration=300):
    current_widget = stacked_widget.currentWidget()
    if current_widget == new_widget:
        return

    width = stacked_widget.frameGeometry().width()
    offset = width if direction == 'left' else -width

    new_widget.setGeometry(offset, 0, stacked_widget.width(), stacked_widget.height())
    stacked_widget.addWidget(new_widget)

    anim_old = QPropertyAnimation(current_widget, b"geometry")
    anim_old.setDuration(duration)
    anim_old.setEasingCurve(QEasingCurve.OutCubic)
    anim_old.setStartValue(current_widget.geometry())
    anim_old.setEndValue(QRect(-offset, 0, current_widget.width(), current_widget.height()))

    anim_new = QPropertyAnimation(new_widget, b"geometry")
    anim_new.setDuration(duration)
    anim_new.setEasingCurve(QEasingCurve.OutCubic)
    anim_new.setStartValue(QRect(offset, 0, new_widget.width(), new_widget.height()))
    anim_new.setEndValue(QRect(0, 0, stacked_widget.width(), stacked_widget.height()))

    anim_old.start()
    anim_new.start()

    anim_new.finished.connect(lambda: stacked_widget.setCurrentWidget(new_widget))

    # Prevenir garbage collection
    new_widget._slide_anim = (anim_old, anim_new)

def fade_to_widget(stacked_widget, new_widget, duration=400):
    stacked_widget.addWidget(new_widget)
    stacked_widget.setCurrentWidget(new_widget)

    effect = QGraphicsOpacityEffect()
    new_widget.setGraphicsEffect(effect)

    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(duration)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.start()

    # Prevenir garbage collection
    new_widget._fade_anim = anim
