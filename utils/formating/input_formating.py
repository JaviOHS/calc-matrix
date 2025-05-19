from PySide6.QtGui import QTextCharFormat, QFont
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
