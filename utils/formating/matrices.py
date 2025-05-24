from .base import clean_number
from numpy import ndarray

def format_vector(v):
    """Formatea vectores/matrices para visualización"""
    if isinstance(v, (list, tuple, ndarray)):
        if len(v) > 0 and isinstance(v[0], (list, tuple, ndarray)):
            # Matriz
            rows = ["[" + ", ".join(clean_number(x) for x in row) + "]" for row in v]
            return "[\n" + ",\n".join(rows) + "\n]"
        else:
            # Vector
            return "[" + ", ".join(clean_number(x) for x in v) + "]"
    return clean_number(v)
