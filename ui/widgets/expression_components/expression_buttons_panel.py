from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QTextEdit

class ExpressionButtonsPanel(QWidget):
    """Panel de botones para insertar símbolos matemáticos"""
    
    def __init__(self, text_edit: QTextEdit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.setup_ui()
    
    def setup_ui(self):
        symbols = [
            ("^", "^"), ("√", "sqrt("), ("π", "pi"), ("e", "e"), ("ln", "ln("),
            ("log", "log("), ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
            ("y'", "y'(x)"), ("y''", "y''(x)"), ("=", "="), 
            ("+", "+"), ("-", "-"), ("*", "*"), ("/", "/"),
            ("(", "("), (")", ")"), ("{", "{"), ("}", "}"),
            ("[", "["), ("]", "]"), ("{", "{"), ("}", "}"),
        ]

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        for index, (label, insert_text) in enumerate(symbols):
            button = QPushButton(label)
            button.setMinimumSize(42, 42)
            button.setObjectName("ctaButton")
            button.setStyleSheet("font-size: 14px;")
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda _, text=insert_text: self.insert_symbol(text))
            layout.addWidget(button, index // 8, index % 8)

    def insert_symbol(self, text):
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()