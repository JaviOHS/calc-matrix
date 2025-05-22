from enum import Enum
import platform
from typing import Dict

class FontWeight(Enum):
    """Pesos de fuente según el sistema operativo."""
    LIGHT = "300"
    REGULAR = "400"
    MEDIUM = "500"
    SEMI_BOLD = "600"
    BOLD = "700"
    EXTRA_BOLD = "800"

class FontWeightManager:
    """Gestor de pesos de fuente según el sistema operativo."""
    _os_weight_map: Dict[str, Dict[str, FontWeight]] = {
        "Windows": {
            "default": FontWeight.REGULAR,
            "emphasis": FontWeight.BOLD,
            "strong": FontWeight.EXTRA_BOLD,
            "title": FontWeight.BOLD,
            "button": FontWeight.MEDIUM,
        },
        "Linux": {
            "default": FontWeight.REGULAR,
            "emphasis": FontWeight.MEDIUM,
            "strong": FontWeight.BOLD,
            "title": FontWeight.BOLD,
            "button": FontWeight.MEDIUM,
        },
        "Darwin": {  # macOS
            "default": FontWeight.REGULAR,
            "emphasis": FontWeight.SEMI_BOLD,
            "strong": FontWeight.BOLD,
            "title": FontWeight.BOLD,
            "button": FontWeight.MEDIUM,
        }
    }

    @classmethod
    def get_weight(cls, context: str = "default") -> str:
        """Devuelve el peso de fuente según el contexto y el sistema operativo."""
        os_name = platform.system()
        os_weights = cls._os_weight_map.get(os_name, cls._os_weight_map["Windows"])
        return os_weights.get(context, FontWeight.REGULAR).value