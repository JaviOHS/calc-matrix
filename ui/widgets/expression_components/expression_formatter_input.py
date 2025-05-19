from PySide6.QtGui import QTextCharFormat
from PySide6.QtWidgets import QTextEdit
from utils.formating.input_formating import (
    create_base_format, 
    create_superscript_format,
    add_spacing_around_operators
)
from utils.patterns import BRACKET_COLORS

class ExpressionFormatterInput:
    """Clase para formatear expresiones matemáticas en un QTextEdit"""
    
    def __init__(self, text_edit: QTextEdit):
        self.text_edit = text_edit
        self.bracket_colors = BRACKET_COLORS
        self.setup_formatting()
    
    def setup_formatting(self):
        """Configura el formateo automático de expresiones"""
        self.text_edit.textChanged.connect(self.format_expression)
    
    def format_expression(self):
        """Formatea la expresión matemática en tiempo real"""
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        text = self.text_edit.toPlainText()
        
        # Formatear texto
        text = add_spacing_around_operators(text)
        
        # Actualizar posición del cursor
        new_position = self._calculate_new_cursor_position(position, text)
        
        self._apply_formatting(text, new_position)
    
    def _calculate_new_cursor_position(self, position: int, formatted_text: str) -> int:
        """Calcula la nueva posición del cursor después del formateo"""
        if position > 0:
            original_slice = self.text_edit.toPlainText()[:position]
            formatted_slice = add_spacing_around_operators(original_slice)
            position += len(formatted_slice) - len(original_slice)
        return min(position, len(formatted_text))
    
    def _apply_formatting(self, text: str, cursor_position: int):
        """Aplica el formateo al texto"""
        self.text_edit.blockSignals(True)
        self.text_edit.clear()
        
        new_cursor = self.text_edit.textCursor()
        base_format = create_base_format()
        super_format = create_superscript_format(base_format)
        bracket_stack = []
        
        i = 0
        while i < len(text):
            if text[i] == '^':
                self._handle_superscript(text, i, new_cursor, base_format, super_format)
                i = self._skip_superscript(text, i)
            elif text[i] == '(':
                self._handle_opening_bracket(new_cursor, bracket_stack, base_format)
                i += 1
            elif text[i] == ')':
                self._handle_closing_bracket(new_cursor, bracket_stack, base_format)
                i += 1
            else:
                new_cursor.insertText(text[i], base_format)
                i += 1
        
        # Restaurar cursor
        new_cursor.setPosition(cursor_position)
        self.text_edit.setTextCursor(new_cursor)
        self.text_edit.blockSignals(False)
    
    def _handle_superscript(self, text: str, pos: int, cursor, base_format, super_format):
        cursor.insertText(text[pos], base_format)
        pos += 1
        while pos < len(text) and text[pos].isdigit():
            cursor.insertText(text[pos], super_format)
            pos += 1
    
    def _skip_superscript(self, text: str, pos: int) -> int:
        pos += 1
        while pos < len(text) and text[pos].isdigit():
            pos += 1
        return pos
    
    def _handle_opening_bracket(self, cursor, bracket_stack, base_format):
        bracket_level = len(bracket_stack)
        color_index = bracket_level % len(self.bracket_colors)
        bracket_format = QTextCharFormat(base_format)
        bracket_format.setForeground(self.bracket_colors[color_index])
        cursor.insertText('(', bracket_format)
        bracket_stack.append(color_index)
    
    def _handle_closing_bracket(self, cursor, bracket_stack, base_format):
        if bracket_stack:
            color_index = bracket_stack.pop()
            bracket_format = QTextCharFormat(base_format)
            bracket_format.setForeground(self.bracket_colors[color_index])
            cursor.insertText(')', bracket_format)
        else:
            cursor.insertText(')', base_format)
