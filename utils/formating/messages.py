from utils.core.font_weight_manager import FontWeightManager
bold = FontWeightManager.get_weight("strong")

def format_warning(message):
    """Formatea un mensaje de advertencia con el estilo estándar."""
    return f"<span style='color: orange; font-weight: {bold};'>{message}</span>"

def format_error(message):
    """Formatea un mensaje de error con el estilo estándar."""
    return f"<span style='color: red; font-weight: {bold};'>{message}</span>"

class DialogFormat:
    WARNING = ("🟡 VALIDACIÓN", "#ffcc32")
    ERROR = ("🔴 ERROR", "#f44336")
    INFO = ("ℹ️ INFO", "#2196F3")
    SUCCESS = ("✅ ÉXITO", "#4CAF50")