import re
import sympy as sp
import numpy as np

def format_math_expression(expr, result, operation_type="generic"):
    """
    Formatea expresiones matemáticas (polinomios, vectores, matrices) de manera consistente
    """
    def clean_number(n):
        """Formatea números para mostrar enteros como enteros y floats con decimales significativos"""
        if isinstance(n, complex):
            real = clean_number(n.real)
            imag = clean_number(n.imag)
            return f"{real} {'+' if n.imag >= 0 else '-'} {imag}i"
        
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
                return "[" + ",\n ".join(rows) + "]"
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
        
        # Resto de sustituciones
        text = re.sub(r'(\d+)\s*/\s*(\d+)([a-zA-Z])', r'(\1/\2)·\3', text)
        text = re.sub(r'([a-zA-Z])\(', r'\1·(', text)
        text = re.sub(r'(?<=[^\^<])([+\-*/=])', r' \1 ', text)  # Modificado para ignorar tags HTML
        text = re.sub(r'(\d)\s*[\*·]\s*([a-zA-Z])', r'\1\2', text)
        
        return text
    
    def format_roots_result(expression, roots):
        """Formatea las raíces del polinomio y las muestra."""
        def to_unicode_repr(expr):
            return (
                str(expr)
                .replace("sqrt", "√")
                .replace("*", "")
                .replace("I", "i")  # Para raíces complejas
            )

        formatted_expr = format_polynomial(expression)

        # Encabezado del resultado
        header = (
            f"<div>"
            f"<span style='font-weight: 600; color: #4CAF50;'>🟢 Resultado de la operación:</span>"
            f"<div style='font-weight: 600;'>"
            f"Polinomio: <span style='font-family: Cambria Math; color: #666;'>{formatted_expr}</span><br>"
            f"</div>"
        )

        title_html = (
            "<span style='font-weight: 600;'>"
            "Raíces encontradas:</span><br>"
        )

        roots_html = ""
        for idx, root in enumerate(roots):
            try:
                root_expr = to_unicode_repr(root)

                # Evaluar numéricamente
                approx = sp.N(root)
                approx_str = f"{float(approx):.4f}" if approx.is_real else str(approx.evalf(4))

                roots_html += (
                    f"<span style='font-family: Cambria Math; color: #4CAF50;'>"
                    f"x<sub>{idx + 1}</sub> ≈ {approx_str}&nbsp;&nbsp;&nbsp;&nbsp;(≡ {root_expr})"
                    f"</span><br>"
                )

            except Exception as e:
                roots_html += (
                    f"<span style='font-family: Cambria Math; color: red;'>"
                    f"x<sub>{idx + 1}</sub>: Error al calcular esta raíz. "
                    f"Detalles: {str(e)}"
                    f"</span><br>"
                )

        return header + title_html + roots_html + "</div>"
    
    # Formatear según el tipo de operación
    if operation_type in ["vector", "matrix"]:
        formatted_expr = format_polynomial(expr)
        formatted_result = format_vector(result)
        
        return (
            f"<div>"
            f"<span style='font-weight: 600; color: #4CAF50;'>🟢 Resultado de la operación:</span>"
            f"<div style='margin: 8px 0; font-family: Cambria Math;'>"
            f"<span>{formatted_expr}</span> = <span style='color: #2196F3;'>{formatted_result}</span>"
            f"</div>"
            f"</div>"
        )
    elif operation_type == "roots":
        return format_roots_result(expr, result)
    else:  # Polinomios y otros
        formatted_expr = format_polynomial(expr)
        formatted_result = format_polynomial(result)
        
        return (
            f"<div>"
            f"<span style='font-weight: 600; color: #4CAF50;'>🟢 Resultado de la operación:</span>"
            f"<div style='margin: 8px 0; font-family: Cambria Math, serif;'>"
            f"<span>{formatted_expr}</span> = <span style='color: #2196F3;'>{formatted_result}</span>"
            f"</div>"
            f"</div>"
        )
    