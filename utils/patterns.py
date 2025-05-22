from PySide6.QtGui import QColor

"""Configuraciones y patrones para formateo de texto matemático y ecuaciones diferenciales"""

# Símbolos matemáticos básicos y sus reemplazos
MATH_SYMBOLS = {
    "·": "*",
    "−": "-", 
    "×": "*", 
    "÷": "/", 
    "^": "**",
    "[": "(", 
    "]": ")", 
    "{": "(", 
    "}": ")", 
    "sen": "sin",
    "=": "=="
}

# Patrones para ecuaciones diferenciales
ODE_PATTERNS = {
    # Patrones de derivadas básicas con más variantes
    r'd\s*y\s*/\s*d\s*x': 'Derivative(y(x), x)',
    r"dy/dx": "Derivative(y(x), x)",
    r"y'(?!\()\s*\(?x?\)?": "Derivative(y(x), x)",  # Acepta y'(x) y y'
    r"y'\s*\(x\)": "Derivative(y(x), x)",  # Específicamente para y'(x)
    
    # Patrones de segundas derivadas con más variantes
    r"d²y/dx²": "Derivative(y(x), (x, 2))",
    r"d\^?2y/dx\^?2": "Derivative(y(x), (x, 2))",
    r"y''(?!\()\s*\(?x?\)?": "Derivative(y(x), (x, 2))",  # Acepta y''(x) y y''
    
    # Corrección de notaciones incorrectas comunes
    r"dy\s+x": "dy/dx",  # Corrige "dy x" a "dy/dx"
    r"dy\s*=": "dy/dx =",  # Añade el denominador faltante
    
    # Limpieza de variables sueltas
    r'\by\b(?!\s*[\(\'])': "y(x)",
    r'\b(dx|dy)\b(?!/)': ''
}

# Patrones de visualización para formateo
DISPLAY_PATTERNS = {
    r'Derivative\(y\(x\),\s*\(x,\s*2\)\)': "y''(x)",
    r'Derivative\(y\(x\),\s*x\)': "y'(x)",
    r'exp\(x\)': "e^x",
    r'exp\(-x\)': "e^(-x)",
    r'C(\d)': lambda m: f'C{chr(8320 + int(m.group(1)))}'  # Subíndices unicode
}

# Caracteres especiales y sus descripciones
SPECIAL_CHARS = {
    '$': 'símbolo de dólar ($)',
    '%': 'símbolo de porcentaje (%)',
    '@': 'arroba (@)',
    '&': 'ampersand (&)',
    '#': 'numeral (#)',
    '!': 'exclamación (!)',
    '?': 'interrogación (?)'
}

# Conjunto de caracteres permitidos básicos
ALLOWED_CHARS = set("0123456789.+-*·/()[] abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ^=π")

# Conjunto de caracteres para ecuaciones diferenciales (incluye comilla simple)
ALLOWED_DIFFERENTIAL_CHARS = ALLOWED_CHARS.union(set("'"))

# Paleta de colores consistente
COLORS = {
    'primary': '#037df5',    # Azul principal
    'secondary': '#fc7e00',  # Naranja para encabezados secundarios
    'success': '#02dc0d',    # Verde para resultados exitosos
    'error': '#D32F2F',      # Rojo para errores
    'neutral': '#616161',    # Gris para texto auxiliar
    'light': '#e0e0e0'       # Gris claro
}

# Colores para paréntesis anidados
BRACKET_COLORS = [
    QColor(255, 165, 0),  # Naranja
    QColor(0, 0, 255),    # Azul
    QColor(0, 128, 0),    # Verde
    QColor(128, 0, 128),  # Púrpura
    QColor(255, 0, 0),    # Rojo
]

# Iconos para diferentes tipos de secciones
ICONS = {
    'input': '🔍',
    'operation': '🔸',
    'result': '🔹',
    'pin': '📌',
    'error': '❌',
    'matrix': '📊',
    'green': '✔️',
    'red': '♦️',
}
