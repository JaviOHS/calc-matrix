import re

def is_valid_number(value):
    """Verifica si el valor es un número válido (puede ser negativo, flotante o entero)."""
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
