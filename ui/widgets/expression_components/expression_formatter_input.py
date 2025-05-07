from PySide6.QtGui import QTextCharFormat, QFont
from PySide6.QtWidgets import QTextEdit

class ExpressionFormatterInput:
    """Clase para formatear expresiones matemáticas en un QTextEdit"""
    
    def __init__(self, text_edit: QTextEdit):
        self.text_edit = text_edit
        self.setup_formatting()
    
    def setup_formatting(self):
        """Configura el formateo automático de expresiones"""
        self.text_edit.textChanged.connect(self.format_expression)
    
    def format_expression(self):
        """Formatea la expresión matemática en tiempo real"""
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        text = self.text_edit.toPlainText()
        self.text_edit.blockSignals(True)

        # Construir un nuevo documento formateado
        self.text_edit.clear()
        new_cursor = self.text_edit.textCursor()

        base_format = QTextCharFormat()
        base_format.setFont(QFont("Cambria Math", 14))

        super_format = QTextCharFormat(base_format)
        super_format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        i = 0
        while i < len(text):
            if text[i] == '^':
                new_cursor.insertText('^', base_format)
                i += 1
                # Formatear superíndices
                while i < len(text) and text[i].isdigit():
                    new_cursor.insertText(text[i], super_format)
                    i += 1
            else:
                new_cursor.insertText(text[i], base_format)
                i += 1

        # Restaurar posición del cursor
        new_cursor.setPosition(min(position, len(self.text_edit.toPlainText())))
        self.text_edit.setTextCursor(new_cursor)
        self.text_edit.blockSignals(False)