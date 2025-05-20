from PySide6.QtGui import QTextCharFormat, QFont
from PySide6.QtWidgets import QTextEdit
import re
from typing import List, Tuple

def create_base_format() -> QTextCharFormat:
    """Crea el formato base para el texto"""
    base_format = QTextCharFormat()
    base_format.setFont(QFont("Cambria Math", 14))
    return base_format

def create_superscript_format(base_format: QTextCharFormat) -> QTextCharFormat:
    """Crea el formato para superíndices"""
    super_format = QTextCharFormat(base_format)
    super_format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
    return super_format

def setup_text_edit_signals(text_edit: QTextEdit, format_callback, limit_callback):
    """
    Configura las señales para el formateo y límite de caracteres del QTextEdit.
    
    Args:
        text_edit (QTextEdit): El widget al que se aplicarán las señales
        format_callback: Función de callback para el formateo
        limit_callback: Función de callback para el límite de caracteres
    """
    text_edit.textChanged.connect(limit_callback)
    text_edit.textChanged.connect(format_callback)

def enforce_character_limit(text_edit: QTextEdit, char_limit: int):
    """
    Verifica y aplica el límite de caracteres en el QTextEdit.
    
    Args:
        text_edit (QTextEdit): El widget a limitar
        char_limit (int): Número máximo de caracteres permitidos
    """
    text = text_edit.toPlainText()
    if len(text) > char_limit:
        text_edit.blockSignals(True)
        text_edit.setPlainText(text[:char_limit])
        text_edit.blockSignals(False)
        
        cursor = text_edit.textCursor()
        cursor.setPosition(char_limit)
        text_edit.setTextCursor(cursor)

def add_spacing_around_operators(text: str) -> str:
    """Añade espacios alrededor de operadores matemáticos"""
    # Reemplazar * por · para multiplicación
    text = text.replace('*', '·')
    
    # Identificar regiones protegidas (exponentes)
    exp_pattern = r'\^\d+'
    exp_matches = list(re.finditer(exp_pattern, text))
    protected_regions = [(m.start(), m.end()) for m in exp_matches]
    
    # Normalizar espacios
    text = normalize_spaces(text)
    
    # Agregar espacios alrededor de operadores
    return format_operators(text, protected_regions)

def normalize_spaces(text: str) -> str:
    """Normaliza los espacios en el texto"""
    normalized = []
    skip_space = False
    
    for char in text:
        if char == ' ':
            if not skip_space:
                normalized.append(' ')
                skip_space = True
        else:
            normalized.append(char)
            skip_space = False
    
    return ''.join(normalized)

def format_operators(text: str, protected_regions: List[Tuple[int, int]]) -> str:
    """Formatea los operadores añadiendo espacios"""
    def is_protected(pos):
        return any(start <= pos < end for start, end in protected_regions)
    
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        
        if i > 0 and char in '+-·/=,' and not is_protected(i):
            if result and result[-1] != ' ':
                result.append(' ')
            result.append(char)
            if i + 1 < len(text) and text[i + 1] != ' ':
                result.append(' ')
        else:
            result.append(char)
        i += 1
    
    return ''.join(result)
