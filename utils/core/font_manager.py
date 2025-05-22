from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
from PySide6.QtGui import QFontDatabase

@dataclass
class FontVariant:
    weight: str
    file_name: str
    purpose: str

class FontFamily:
    def __init__(self, name: str, variants: List[FontVariant]):
        self.name = name
        self.variants = variants
        self._loaded_fonts: Dict[str, int] = {}

    def load(self, resource_path_fn) -> bool:
        success = True
        for variant in self.variants:
            font_path = resource_path_fn(f"assets/fonts/{variant.file_name}")
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id == -1:
                print(f"Error loading font: {variant.file_name}")
                success = False
            else:
                self._loaded_fonts[variant.weight] = font_id
        return success