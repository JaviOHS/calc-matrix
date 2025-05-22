import re
import sympy as sp
from .base import create_section
from .polynomials import format_polynomial
from utils.patterns import DISPLAY_PATTERNS, COLORS, ICONS

def standardize_ode_equation(equation, is_symbolic=True, preserve_original=True, is_numerical=False):
    """
    Estandariza la representación de una ecuación diferencial para mostrarlas
    de forma consistente tanto en métodos analíticos como numéricos.
    """
    # Extraer información original y texto de la ecuación según el tipo
    original_text = ""
    rhs_text = ""
    symbolic_repr = None # Para manejo de ecuación en gráficas
    
    # Caso 1: Entrada es una tupla del tipo (función, texto_rhs) de métodos numéricos - EXPANDIR SI ES NECESARIO
    if isinstance(equation, tuple) and len(equation) == 2 and callable(equation[0]):
        _, rhs_text = equation
        original_text = rhs_text
        
    if preserve_original:
        return {"display": equation, "original": original_text, "symbolic": symbolic_repr}
    else:
        return equation
    
def format_diff_eq(equation, solution):
    """Formateador especializado para ecuaciones diferenciales"""
    html_result = []
    try:
        if hasattr(equation, 'lhs') and hasattr(equation, 'rhs'):
            lhs = equation.lhs
            rhs = equation.rhs
        else:
            # Si es una tupla (lhs, rhs)
            lhs, rhs = equation
            
        # Procesar ambos lados de la ecuación
        eq_text = f"{lhs} = {rhs}"
        
        # Procesar la solución
        if hasattr(solution, 'rhs'):
            sol_text = sp.sstr(solution.rhs, full_prec=False)
            sol_text = sol_text.replace("Eq(y(x),", "y(x) =")
        else:
            sol_text = str(solution)
        # Sustituir derivados simbólicos
        eq_text = eq_text.replace("Derivative(y(x), (x, 2))", "y''(x)")
        eq_text = eq_text.replace("Derivative(y(x), x)", "y'(x)")
        
        # Formatear solución
        sol_text = sol_text.replace("Eq(y(x),", "y(x) =")
        sol_text = sol_text.replace("exp(x)", "e<sup>x</sup>")
        sol_text = sol_text.replace("exp(-x)", "e<sup>-x</sup>")
        sol_text = re.sub(r'C(\d)', lambda m: f'C{chr(8320 + int(m.group(1)))}', sol_text)
        
        # Aplicar formato polinomial para superíndices y operadores
        eq_text = format_polynomial(eq_text)
        sol_text = format_polynomial(sol_text)
        # Aplicar patrones de visualización
        for pattern, replacement in DISPLAY_PATTERNS.items():
            if callable(replacement):
                eq_text = re.sub(pattern, replacement, eq_text)
                sol_text = re.sub(pattern, replacement, sol_text)
            else:
                eq_text = re.sub(pattern, replacement, eq_text)
                sol_text = re.sub(pattern, replacement, sol_text)
        html_result.append(create_section('Ecuación Diferencial:<br>', eq_text, COLORS['secondary'], ICONS['operation']))
        html_result.append(create_section('Solución General:<br>', sol_text, COLORS['primary'], ICONS['result']))
        
        return "".join(html_result)
    except AttributeError:
        return create_section('Error:', 'La ecuación no está bien formada como objeto Eq', COLORS['error'], ICONS['error'])
    
def format_numerical_method(result, method_name):
    """Formato unificado para resultados de métodos numéricos con diseño oscuro y centrado"""
    from utils.core.font_weight_manager import FontWeightManager
    bold = FontWeightManager.get_weight("strong")
    table_html = (
        "<div style='margin: 15px 0; padding: 15px; border-radius: 8px; "
        "display: flex; justify-content: center; align-items: center;'>"
        "<table style='width: 80%; border-collapse: collapse; text-align: center;'>"
        "<thead>"
        "<tr>"
        "<th style='padding: 12px; border-bottom: 2px solid #ff8103; "
        f"color: #D8DEE9; font-weight: {bold}; width: 50%;'>x</th>"
        "<th style='padding: 12px; border-bottom: 2px solid #ff8103; "
        f"color: #D8DEE9; font-weight: {bold}; width: 50%;'>y</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
    )
    
    for x, y in result:
        table_html += (
            "<tr>"
            f"<td style='padding: 8px; border-bottom: 1px solid #2E3440; "
            f"color: #D8DEE9;'>{x:.6f}</td>"
            f"<td style='padding: 8px; border-bottom: 1px solid #2E3440; "
            f"color: #D8DEE9;'>{y:.6f}</td>"
            "</tr>"
        )
    
    table_html += (
        "</tbody>"
        "</table>"
        "</div>"
    )
    
    return create_section(
        f'Tabla de solución numérica:',
        table_html, 
        COLORS['secondary'], 
        ICONS['operation']
    )