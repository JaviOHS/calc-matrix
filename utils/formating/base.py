import numpy as np
from utils.core.font_weight_manager import FontWeightManager

def create_section(title, content, color, icon=None):
    """Helper para crear secciones consistentes con peso de fuente dinámico"""
    icon_html = f"{icon} " if icon else ""
    font_weight = FontWeightManager.get_weight("strong")
    
    # Procesar etiquetas <b> con el peso de fuente del sistema
    content = content.replace("<b>", f"<b style='font-weight: {font_weight}'>")
    
    return (
        f"<div style='margin-bottom: 15px;'>"
        f"<span style='font-weight: {font_weight}; color: {color}; margin-bottom: 5px;'>{icon_html} {title}</span>"
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
