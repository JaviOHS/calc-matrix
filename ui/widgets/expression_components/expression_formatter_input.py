from PySide6.QtGui import QTextCharFormat, QFont, QColor
from PySide6.QtWidgets import QTextEdit
import re

class ExpressionFormatterInput:
    """Clase para formatear expresiones matemáticas en un QTextEdit"""
    
    def __init__(self, text_edit: QTextEdit):
        self.text_edit = text_edit
        # Colores para los diferentes niveles de paréntesis
        self.bracket_colors = [
            QColor(255, 165, 0),
            QColor(0, 0, 255),
            QColor(0, 128, 0),
            QColor(128, 0, 128),
            QColor(255, 0, 0),
        ]
        self.setup_formatting()
    
    def setup_formatting(self):
        """Configura el formateo automático de expresiones"""
        self.text_edit.textChanged.connect(self.format_expression)
    
    def format_expression(self):
        """Formatea la expresión matemática en tiempo real"""
        cursor = self.text_edit.textCursor()
        position = cursor.position()
        text = self.text_edit.toPlainText()
        
        # Guardar el texto original para calcular el desplazamiento del cursor
        original_text = text
        
        # Aplicar espaciado alrededor de operadores
        text = self.add_spacing_around_operators(text)
        
        # Calcular la nueva posición del cursor teniendo en cuenta los espacios añadidos a la izquierda del cursor
        new_position = position
        if position > 0:
            # Contar espacios añadidos antes de la posición original
            original_slice = original_text[:position]
            formatted_slice = self.add_spacing_around_operators(original_slice)
            new_position += len(formatted_slice) - len(original_slice)
        
        self.text_edit.blockSignals(True)

        # Construir un nuevo documento formateado
        self.text_edit.clear()
        new_cursor = self.text_edit.textCursor()

        base_format = QTextCharFormat()
        base_format.setFont(QFont("Cambria Math", 14))

        super_format = QTextCharFormat(base_format)
        super_format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        # Stack para llevar el seguimiento de paréntesis abiertos
        bracket_stack = []

        i = 0
        while i < len(text):
            if text[i] == '^':
                new_cursor.insertText('^', base_format)
                i += 1
                # Formatear superíndices
                while i < len(text) and text[i].isdigit():
                    new_cursor.insertText(text[i], super_format)
                    i += 1
            elif text[i] == '(':
                # Aplicar color según el nivel de anidamiento
                bracket_level = len(bracket_stack)
                color_index = bracket_level % len(self.bracket_colors)
                bracket_format = QTextCharFormat(base_format)
                bracket_format.setForeground(self.bracket_colors[color_index])
                
                new_cursor.insertText('(', bracket_format)
                bracket_stack.append(color_index)
                i += 1
            elif text[i] == ')':
                # Usar el mismo color que el paréntesis de apertura correspondiente
                if bracket_stack:
                    color_index = bracket_stack.pop()
                    bracket_format = QTextCharFormat(base_format)
                    bracket_format.setForeground(self.bracket_colors[color_index])
                    new_cursor.insertText(')', bracket_format)
                else:
                    # Si no hay paréntesis abiertos, usar el color base
                    new_cursor.insertText(')', base_format)
                i += 1
            else:
                new_cursor.insertText(text[i], base_format)
                i += 1

        # Restaurar posición del cursor teniendo en cuenta los espacios añadidos
        new_position = min(new_position, len(self.text_edit.toPlainText()))
        new_cursor.setPosition(new_position)
        self.text_edit.setTextCursor(new_cursor)
        self.text_edit.blockSignals(False)
    
    def add_spacing_around_operators(self, text):
        """Añade espacios alrededor de operadores matemáticos para mejorar la legibilidad"""
        # Reemplazar * por · para multiplicación
        text = text.replace('*', '·')
        
        # No agregar espacios dentro de exponentes
        # Primero identificamos los exponentes
        exp_pattern = r'\^\d+'
        exp_matches = list(re.finditer(exp_pattern, text))
        protected_regions = [(m.start(), m.end()) for m in exp_matches]
        
        # Función para verificar si una posición está en una región protegida
        def is_protected(pos):
            return any(start <= pos < end for start, end in protected_regions)
        
        # Primero, normalizar espacios existentes alrededor de operadores - Eliminar espacios múltiples y normalizar espaciado
        normalized = []
        i = 0
        skip_space = False
        
        while i < len(text):
            # Saltarse espacios redundantes
            if text[i] == ' ':
                if not skip_space:
                    normalized.append(' ')
                    skip_space = True
            else:
                normalized.append(text[i])
                skip_space = False
            i += 1
        
        text = ''.join(normalized)
        
        # Volver a calcular las regiones protegidas después de la normalización
        exp_matches = list(re.finditer(exp_pattern, text))
        protected_regions = [(m.start(), m.end()) for m in exp_matches]
        
        # Agregar espacios alrededor de operadores +, -, ·, / y =
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            
            if i > 0 and char in '+-·/=,' and not is_protected(i):
                # Verificar si ya hay un espacio antes del operador
                if result and result[-1] != ' ':
                    result.append(' ')
                
                # Añadir el operador
                result.append(char)
                
                # Verificar si ya hay un espacio después del operador
                if i + 1 < len(text) and text[i + 1] != ' ':
                    result.append(' ')
            else:
                result.append(char)
            i += 1
        
        return ''.join(result)
    