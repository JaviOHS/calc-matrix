import re
import sympy as sp
import numpy as np

# Paleta de colores consistente
COLORS = {
    'primary': '#037df5',    # Azul principal
    'secondary': '#fc7e00',  # Naranja para encabezados secundarios
    'success': '#02dc0d',    # Verde para resultados exitosos
    'error': '#D32F2F',      # Rojo para errores
    'neutral': '#616161',    # Gris para texto auxiliar
    'light': '#e0e0e0'       # Gris claro
}

# Iconos para diferentes tipos de secciones
ICONS = {
    'input': '🔍',
    'operation': '🟠',
    'result': '🔵',
    'roots': '📌',
    'error': '❌',
    'matrix': '📊',
}

def create_section(title, content, color, icon=None):
    """Helper para crear secciones consistentes"""
    icon_html = f"{icon} " if icon else ""
    return (
        f"<div style='margin-bottom: 15px;'>"
        f"<span style='font-weight: bold; color: {color}; margin-bottom: 5px;'>{icon_html} {title}</span>"
        f"<span style='margin-left: 15px;'>{content}</span>"
        f"</div>"
    )

def format_math_expression(expr, result, operation_type="generic", method=None):
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
    
    def format_vector(v):
        """Formatea vectores/matrices para visualización"""
        if isinstance(v, (list, tuple, np.ndarray)):
            if len(v) > 0 and isinstance(v[0], (list, tuple, np.ndarray)):
                # Matriz
                rows = ["[" + ", ".join(clean_number(x) for x in row) + "]" for row in v]
                return "[\n" + ",\n".join(rows) + "\n]"
            else:
                # Vector
                return "[" + ", ".join(clean_number(x) for x in v) + "]"
        return clean_number(v)
    
    def format_polynomial(text):
        """Formatea expresiones polinomiales con superíndices HTML"""
        text = str(text).strip()
        text = text.replace('**', '^').replace('*', '·')
        
        # Convertir exponentes a superíndices HTML
        text = re.sub(r'\^(\d+)', r'<sup>\1</sup>', text)
        
        # Mejorar formato de fracciones y productos
        text = re.sub(r'(\d+)\s*/\s*(\d+)([a-zA-Z])', r'(\1/\2)·\3', text)
        text = re.sub(r'(?<![a-zA-Z])([a-zA-Z]{2,})\(', r'\1·(', text)
        text = re.sub(r'(?<=[^\^<])([+\-*/=])', r' \1 ', text)
        text = re.sub(r'(\d)\s*[\*·]\s*([a-zA-Z])', r'\1\2', text)
        text = re.sub(r'exp·?\(([^)]+)\)', r'e<sup>\1</sup>', text)

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
        
        html_result.append(create_section('Raíces encontradas:', roots_html, COLORS['primary'], ICONS['roots']))
        
        return "".join(html_result)

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

            html_result.append(create_section('Ecuación Diferencial:<br>', eq_text, COLORS['secondary'], ICONS['operation']))
            html_result.append(create_section('Solución General:<br>', sol_text, COLORS['primary'], ICONS['result']))
            
            return "".join(html_result)
        except AttributeError:
            return create_section('Error:', 'La ecuación no está bien formada como objeto Eq', COLORS['error'], ICONS['error'])

    def format_numerical_method(result, method_name):
        """Formato unificado para resultados de métodos numéricos (Euler, Heun, etc.)"""
        table_html = (
            "<div style='margin-left: 15px;'>"
            "<table border='1' style='border-collapse: collapse; width: 100%;'>"
            "<tr style='background-color: #616161; color: #f4ffff;'><th>x</th><th>y</th></tr>"
        )
        
        for x, y in result:
            table_html += f"<tr><td>{x:.4f}</td><td>{y:.4f}</td></tr>"
        
        table_html += "</table></div>"
        
        return create_section(f'Solución por Método de {method_name}:', table_html, COLORS['secondary'], ICONS['operation'])

    # Formatear según el tipo de operación
    if operation_type in ["vector", "matrix"]:
        formatted_expr = format_polynomial(expr)
        formatted_result = format_vector(result)
        
        return (
            create_section('Operación con Vectores/Matrices: ', formatted_expr, COLORS['secondary'], ICONS['matrix']) +
            create_section('Resultado: ', formatted_result, COLORS['primary'], ICONS['result'])
        )
        
    elif operation_type == "roots":
        return format_roots_result(expr, result)
    
    elif operation_type == "ecuaciones_diferenciales":
        # Manejar todos los métodos numéricos de forma genérica
        if method in ["euler", "heun", "rk4"]:
            # Convertir nombre interno a nombre presentable
            method_names = {
                "euler": "Euler",
                "heun": "Heun", 
                "rk4": "Runge-Kutta 4º Orden"
            }
            method_display = method_names.get(method, method.capitalize())
            return format_numerical_method(result, method_display)
        else:
            # Para soluciones analíticas
            return format_diff_eq(expr, result)
    
    else:  # Polinomios y expresiones genéricas
        formatted_expr = format_polynomial(expr)
        formatted_result = format_polynomial(result)
        
        return (
            create_section('Expresión Original: ', formatted_expr, COLORS['secondary'], ICONS['operation']) +
            create_section('Resultado Simplificado: ', formatted_result, COLORS['primary'], ICONS['result'])
        )
