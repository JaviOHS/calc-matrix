import re

def validate_positive_integer(value):
    """Validates that the input is a positive integer."""
    if not isinstance(value, int) or value <= 0:
        raise ValueError("El valor debe ser un número entero positivo.")

def validate_range(value, min_value, max_value):
    """Validates that the input is within a specified range."""
    if not (min_value <= value <= max_value):
        raise ValueError(f"El valor debe estar entre {min_value} y {max_value}.")

def validate_algorithm_choice(choice, valid_choices):
    """Validates that the chosen algorithm is valid."""
    if choice not in valid_choices:
        raise ValueError(f"Elección de algoritmo no válida. Debe ser uno de: {', '.join(valid_choices)}.")

def is_valid_number(value):
    """Checks if a value is a valid number."""
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def exponents_validator(expression: str, max_exponente: int = 1000) -> bool:
    """
    Devuelve True si los exponentes están dentro del límite permitido, False si no.
    """
    # Busca expresiones del tipo x^123456 o x**123456
    exponentes = re.findall(r'x\^(\d+)|x\*\*(\d+)', expression)
    exponentes = [int(exp) for group in exponentes for exp in group if exp]

    # Verifica si algún exponente supera el límite
    for exp in exponentes:
        if exp > max_exponente:
            return False
    return True

def validate_characters(expression: str, allowed_chars: set, special_chars_map: dict) -> tuple[bool, str]:
    """Valida que la expresión solo contenga caracteres permitidos."""
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
    
    # Normalizar espacios alrededor de operadores
    expression = re.sub(r'\s*([+\-*/^])\s*', r' \1 ', expression)
    
    # Verificar operadores consecutivos
    if re.search(r'[+\-*/^]{2,}', expression): 
        return False, "Operadores consecutivos no permitidos."
    
    # Verificar funciones matemáticas vacías
    if re.search(r'\w+\(\s*\)', expression): 
        return False, "Funciones matemáticas vacías no permitidas."
    
    # Verificar términos mal formados
    if re.search(r'\d+[a-zA-Z]+\d+[a-zA-Z]+', expression): 
        return False, "Expresión mal formada. Revise los términos y use * para multiplicación."
    
    return True, ""

def validate_symbols(expr: str, allowed_names: set, use_3d: bool = False, is_differential: bool = False) -> tuple[bool, str]:
    """
    Valida los símbolos en la expresión según el tipo de gráfica.
    
    Args:
        expr: Expresión a validar
        allowed_names: Conjunto de nombres permitidos
        use_3d: Indica si es una gráfica 3D
        is_differential: Indica si es una ecuación diferencial
    
    Returns:
        tuple[bool, str]: (es_válido, mensaje_error)
    """
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