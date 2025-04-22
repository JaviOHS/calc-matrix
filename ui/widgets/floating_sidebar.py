from PySide6.QtWidgets import QVBoxLayout, QPushButton, QSizePolicy
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class FloatingSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        self.setObjectName("FloatingSidebar")
        self.buttons = {}

    def add_button(self, text, callback):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setMinimumHeight(36)
        btn.clicked.connect(callback)
        btn.setProperty("class", "sidebar-button")

        self.layout.addWidget(btn)
        self.buttons[text] = btn

    def set_active(self, active_text):
        for text, btn in self.buttons.items():
            is_active = (text == active_text)
            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
