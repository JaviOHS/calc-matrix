import numpy as np

def create_section(title, content, color, icon=None):
    """Helper para crear secciones consistentes"""
    icon_html = f"{icon} " if icon else ""
    return (
        f"<div style='margin-bottom: 15px; font-family: Cambria Math; font-size: 16px;'>"
        f"<span style='font-weight: bold; color: {color}; margin-bottom: 5px;'>{icon_html} {title}</span>"
        f"<span style='margin-left: 15px;'>{content}</span>"
        f"</div>"
    )

def clean_number(n):
    """Formatea números para mostrar enteros como enteros y floats con decimales significativos"""
    if isinstance(n, complex):
        real = clean_number(n.real)
        imag = clean_number(abs(n.imag))
        operator = '+' if n.imag >= 0 else '-'
        return f"{real} {operator} {imag}i"
    
    if isinstance(n, (int, np.integer)):
        return str(n)
    
    if isinstance(n, (float, np.floating)):
        formatted = f"{n:.4f}"
        return formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
    
    return str(n)
