import re

def validate_positive_integer(value):
    """Valida que el valor sea un número entero positivo."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError("El valor debe ser un número entero positivo.")

def validate_range(value, min_value, max_value):
    """Valida que el valor esté dentro de un rango específico."""
    if not (min_value <= value <= max_value):
        raise ValueError(f"El valor debe estar entre {min_value} y {max_value}.")
    
def is_valid_number(value):
    """Verifica si el valor es un número válido (entero o decimal)."""
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def exponents_validator(expression: str, max_exponent: int = 1000) -> tuple[bool, str]:
    """Valida que los exponentes estén dentro del límite permitido. Devuelve una tupla (is_valid, error_message)."""
    # Primero, normalizar operadores de multiplicación consecutivos
    normalized_expr = re.sub(r'[\·\*]\s*[\·\*]', '·', expression)
    
    # Eliminar espacios para facilitar la detección
    clean_expr = re.sub(r'\s+', '', normalized_expr)
    
    # Patrones mejorados para detectar exponentes:
    # 1. x^123 o x**123 - formato básico
    # 2. x^(123) o x**(123) - exponentes entre paréntesis
    # 3. x·123, x*123, x·(123) - multiplicación que podría interpretarse como exponente
    patterns = [
        r'[a-zA-Z]\^(\d+)', r'[a-zA-Z]\*\*(\d+)',           # Formato básico
        r'[a-zA-Z]\^\((\d+)\)', r'[a-zA-Z]\*\*\((\d+)\)',   # Exponentes entre paréntesis
        r'[a-zA-Z][\·\*](\d{6,})', r'[a-zA-Z][\·\*]\((\d{6,})\)'   # Multiplicaciones grandes
    ]
    
    exponents = []
    for pattern in patterns:
        try:
            matches = re.findall(pattern, clean_expr)
            exponents.extend([int(exp) for exp in matches if exp and exp.isdigit()])
        except Exception as e:
            # En caso de error en la expresión regular, devolver error explicativo
            return False, f"Error al procesar la expresión: {e}. Revise la sintaxis."
    
    for exp in exponents:
        if exp > max_exponent:
            return False, f"El exponente excede el límite máximo ({max_exponent})."
    
    return True, ""

def validate_characters(expression: str, allowed_chars: set, special_chars_map: dict) -> tuple[bool, str]:
    """Valida que la expresión contenga solo caracteres permitidos."""
    invalid_chars = set()
    for char in expression:
        if char not in allowed_chars:
            invalid_chars.add(char)
    
    if invalid_chars:
        error_chars = []
        for char in invalid_chars:
            if char in special_chars_map:
                error_chars.append(special_chars_map[char])
            else:
                error_chars.append(f"'{char}'")
        
        error_msg = (
            f"Caracteres no permitidos encontrados: {', '.join(error_chars)}.\n"
            "Solo se permiten letras, números y los siguientes símbolos: +, -, *, /, ^, (, ), [, ], ="
        )
        return False, error_msg
    return True, ""

def validate_parentheses(expression: str) -> tuple[bool, str]:
    """Verifica que los paréntesis y corchetes estén balanceados."""
    stack = []
    brackets = {')': '(', ']': '[', '}': '{'}
    
    for char in expression:
        if char in '([':
            stack.append(char)
        elif char in ')]':
            if not stack or stack.pop() != brackets[char]:
                return False, "Los paréntesis en la expresión no están balanceados."
    
    if stack:
        return False, "Los paréntesis en la expresión no están balanceados."
    return True, ""

def validate_expression_syntax(expression: str) -> tuple[bool, str]:
    """Valida la sintaxis básica de una expresión matemática."""
    expression = re.sub(r'\s*([+\-*/^])\s*', r' \1 ', expression) # Normalizar espacios alrededor de operadores
    
    if re.search(r'\w+\(\s*\)', expression): # Verificar funciones matemáticas vacías
        return False, "Funciones matemáticas vacías no permitidas."
    
    if re.search(r'\d+[a-zA-Z]+\d+[a-zA-Z]+', expression): # Verificar términos mal formados
        return False, "Expresión mal formada. Revise los términos y use · para multiplicación."
    
    return True, ""

def validate_symbols(expr: str, allowed_names: set, use_3d: bool = False, is_differential: bool = False) -> tuple[bool, str]:
    """Valida los símbolos en la expresión según el tipo de gráfica."""
    pattern = r'\b([a-zA-Z][a-zA-Z0-9]*)\b'
    found_symbols = set(re.findall(pattern, expr))
    
    # Determinar símbolos permitidos según el contexto
    if use_3d or is_differential:
        allowed_symbols = allowed_names | {"x", "y"}
    else:
        allowed_symbols = allowed_names - {"y"}  # Excluir 'y' solo en gráficas 2D normales
    
    invalid_symbols = found_symbols - allowed_symbols
    if invalid_symbols:
        if "y" in invalid_symbols and not (use_3d or is_differential):
            return False, "La variable 'y' solo está permitida en gráficas 3D y ecuaciones diferenciales."
        else:
            symbols_list = ", ".join(sorted(invalid_symbols))
            return False, f"Símbolos no permitidos: {symbols_list}"
            
    return True, ""