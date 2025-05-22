from typing import Dict, Any
from utils.core.font_weight_manager import FontWeightManager

class StyleManager:
    def __init__(self, resource_path_fn):
        self.resource_path_fn = resource_path_fn
        self._cache: Dict[str, str] = {}
        
    def get_font_variables(self):
        """Obtiene todas las variables de fuente necesarias"""
        return {
            # Familias de fuente
            "FONT_FAMILY": "'Fira Sans'",  # Agregamos comillas
            "MATH_FONT_FAMILY": "'Cambria Math'",  # Agregamos comillas
            
            # Pesos de fuente
            "DEFAULT_WEIGHT": FontWeightManager.get_weight("default"),
            "EMPHASIS_WEIGHT": FontWeightManager.get_weight("emphasis"),
            "STRONG_WEIGHT": FontWeightManager.get_weight("strong"),
            "TITLE_WEIGHT": FontWeightManager.get_weight("title"),
            "BUTTON_WEIGHT": FontWeightManager.get_weight("button"),
            
            # Tamaños de fuente (aseguramos que tengan 'px')
            "BASE_FONT_SIZE": "16px",
            "SMALL_FONT_SIZE": "14px",
            "LARGE_FONT_SIZE": "18px",
            "TITLE_FONT_SIZE": "28px",
            "HERO_FONT_SIZE": "36px",
        }
        
    def load_styles(self, variables: Dict[str, Any] = None) -> str:
        style_files = [
            "base.qss",
            "layout.qss",
            "pages.qss",
            "components.qss",
            "buttons.qss",
            "inputs.qss",
            "scrollbars.qss",
            "dialogs.qss"
        ]
        
        combined_styles = []
        
        for style_file in style_files:
            if style_file not in self._cache:
                file_path = self.resource_path_fn(f"styles/{style_file}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self._cache[style_file] = f.read()
                except FileNotFoundError:
                    print(f"Warning: Style file not found: {style_file}")
                    continue
                    
            combined_styles.append(self._cache[style_file])
        
        final_style = "\n\n".join(combined_styles)
        
        if variables:
            # Usamos replace en lugar de safe_substitute para asegurar que todas las variables se reemplacen
            for key, value in variables.items():
                final_style = final_style.replace(f"{{{{{key}}}}}", str(value))
            
        return final_style