from PySide6.QtWidgets import QWidget, QGridLayout, QTextEdit
from utils.components.action_buttons import ActionButton

class ExpressionButtonsPanel(QWidget):
    """Panel de botones para insertar símbolos matemáticos"""
    
    def __init__(self, text_edit: QTextEdit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.setup_ui()
    
    def setup_ui(self):
        symbols = [
            ("^", "^"), ("√", "sqrt("), ("π", "π"), ("e", "e"), ("ln", "ln("),
            ("log", "log("), ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
            ("x", "x") ,("y'", "y'(x) ="), ("=", "="), 
            ("+", "+"), ("-", "-"), ("·", "·"), ("/", "/"),
            ("( )", "( )"), ("[ ]", "[ ]"),
            ("1", "1"), ("2", "2"), ("3", "3"),
            ("4", "4"), ("5", "5"), ("6", "6"),
            ("7", "7"), ("8", "8"), ("9", "9")
        ]

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        for index, (label, insert_text) in enumerate(symbols):
            button = ActionButton(label,parent=self,object_name="ctaButton")
            button.setMinimumSize(42, 42)
            button.clicked.connect(lambda _, text=insert_text: self.insert_symbol(text))
            layout.addWidget(button, index // 9, index % 9)

    def insert_symbol(self, text):
        cursor = self.text_edit.textCursor()
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFocus()
