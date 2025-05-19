import re
import sympy as sp
from .base import clean_number, create_section
from utils.patterns import COLORS, ICONS

def format_polynomial(text):
    """Formatea expresiones polinomiales con superíndices HTML"""
    text = str(text).strip()
    
    # Eliminar el envoltorio Eq(lhs, rhs) si está presente
    if text.startswith("Eq"):
        text = text[3:-1]  # Remover "Eq(" al inicio y ")" al final
    
    # Reemplazar operadores y símbolos matemáticos
    text = text.replace('**', '^').replace('*', '·')
    
    # Convertir exponentes a superíndices HTML
    text = re.sub(r'\^(\d+)', r'<sup>\1</sup>', text)
    
    # Mejorar formato de fracciones y productos
    text = re.sub(r'(\d+)\s*/\s*(\d+)([a-zA-Z])', r'(\1/\2)·\3', text)
    text = re.sub(r'(?<![a-zA-Z])([a-zA-Z]{2,})\(', r'\1(', text)  # Eliminar el punto entre funciones y paréntesis
    text = re.sub(r'(?<=[^\^<])([+\-*/=])', r' \1 ', text)
    text = re.sub(r'(\d)\s*[\*·]\s*([a-zA-Z])', r'\1\2', text)
    
    # Reemplazar funciones trigonométricas y exponenciales
    text = text.replace("sin(", "sin(").replace("cos(", "cos(").replace("exp(", "e^(")
    
    return text

def format_roots_result(expression, roots):
    """Formatea las raíces del polinomio con presentación mejorada"""
    def to_unicode_repr(expr):
        return (
            str(expr)
            .replace("sqrt", "√")
            .replace("*", "")
            .replace("I", "i")
            .replace(" ", "")
        )
    formatted_expr = format_polynomial(expression)
    html_result = []
    # Encabezado con el polinomio
    html_result.append(create_section('Polinomio: ', formatted_expr, COLORS['secondary'], ICONS['operation']))
    
    # Sección de raíces
    roots_html = "<div style='margin-left: 15px;'>"
    for idx, root in enumerate(roots):
        try:
            root_expr = to_unicode_repr(root)
            approx = sp.N(root)
            
            if approx.is_real:
                approx_str = f"{float(approx):.6f}".rstrip('0').rstrip('.')
            else:
                approx_str = str(approx.evalf(6)).replace('*I', 'i').replace(' ', '')
            
            roots_html += (
                f"<div style='margin: 6px 0;'>"
                f"<span style='color: {COLORS['error']}; font-weight: bold;'>x<sub>{idx + 1}</sub></span> "
                f"≈ <span style='color: {COLORS['success']};'>{approx_str}</span>"
                f"<span style='color: {COLORS['neutral']}; margin-left: 10px;'>(forma exacta: {root_expr})</span>"
                f"</div>"
            )
        except Exception as e:
            roots_html += (
                f"<div style='margin: 6px 0; color: {COLORS['error']};'>"
                f"{ICONS['error']} Error en raíz x<sub>{idx + 1}</sub>: {str(e)}"
                f"</div>"
            )
    roots_html += "</div>"
    
    html_result.append(create_section('Raíces encontradas:', roots_html, COLORS['primary'], ICONS['pin']))
    
    return "".join(html_result)

def format_evaluation_result(expr, results):
    """Formatea los resultados de evaluación de polinomios"""
    html_result = []
    formatted_expr = format_polynomial(expr)
    
    # Crear tabla de resultados
    table_html = (
        "<div style='margin: 8px 0;'>"
        "<table style='border-collapse: collapse; width: auto;'>"
        "<tbody>"
    )
    
    for poly_name, value in results:
        table_html += (
            f"<tr>"
            f"<td style='padding: 5px 10px; color: {COLORS['secondary']}; font-weight: bold;'>{ICONS['pin']} {poly_name}:</td>"
            f"<td style='padding: 5px 10px;'>{clean_number(value)}</td>"
            f"</tr>"
        )
        
    table_html += "</tbody></table></div>"
    
    html_result.append(create_section('Polinomio: ', formatted_expr, COLORS['secondary'], ICONS['operation']))
    html_result.append(create_section('Evaluación: ', table_html, COLORS['primary'], ICONS['result']))
    
    return "".join(html_result)
