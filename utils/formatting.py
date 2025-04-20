import re

def format_polynomial_html(text: str, color="rgba(114, 228, 140, 0.7)") -> str:
    text = text.replace(' ', '')
    formatted = text.replace('+', ' + ').replace('-', ' - ')
    formatted = formatted.replace('*', '·').replace('/', ' ÷ ').replace('**', '^')
    formatted = re.sub(r'\^(\d+)', r'<sup>\1</sup>', formatted)

    return f"<span style='font-family: Cambria Math; color: {color};'>{formatted}</span>"
