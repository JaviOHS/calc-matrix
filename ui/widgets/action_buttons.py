from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
from utils.resources import resource_path
from utils.icon_utils import colored_svg_icon

class ActionButton(QPushButton):
    """
    Componente de botón reutilizable con estilo consistente para la aplicación.
    Incluye soporte para iconos, colores personalizados y tamaños ajustables.
    """
    def __init__(self, text, icon_name=None, icon_color=QColor(28, 44, 66),icon_size=QSize(20, 20), parent=None, object_name="ctaButton"):
        """
        Inicializa un botón de acción estilizado.
        
        Args:
            text (str): Texto a mostrar en el botón
            icon_name (str, optional): Nombre del archivo de icono SVG (sin ruta)
            icon_color (QColor, optional): Color para el icono
            icon_size (QSize, optional): Tamaño del icono
            parent (QWidget, optional): Widget padre
            object_name (str, optional): Nombre del objeto CSS
        """
        super().__init__(text, parent)
        
        # Configuración básica
        self.setObjectName(object_name)
        self.setCursor(Qt.PointingHandCursor)
        
        # Configurar icono si se proporciona
        if icon_name:
            icon_path = resource_path(f"assets/icons/{icon_name}")
            icon = colored_svg_icon(icon_path, icon_color)
            self.setIcon(icon)
            self.setIconSize(icon_size)
            
    @classmethod
    def primary(cls, text, parent=None):
        """Botón primario con icono de flecha (go.svg)"""
        return cls(text, "go.svg", parent=parent)
    
    @classmethod
    def cancel(cls, text="Cancelar", parent=None):
        """Botón de cancelación"""
        return cls(text, "cancel.svg", parent=parent)
    
    @classmethod
    def calculate(cls, text="Calcular", parent=None):
        """Botón de cálculo"""
        return cls(text, "calculator.svg", parent=parent)
    
    @classmethod
    def options(cls, text="Opciones", parent=None):
        """Botón de opciones"""
        return cls(text, "options.svg", parent=parent)
    
    @classmethod
    def icon_only(cls, icon_name, icon_size=QSize(24, 24), parent=None, object_name="iconButton"):
        """Botón solo con icono (sin texto)"""
        return cls("", icon_name, icon_size=icon_size, parent=parent, object_name=object_name)
    
    @classmethod
    def save(cls, text="Guardar", parent=None):
        """Botón para guardar elementos"""
        return cls(text, "save.svg", parent=parent)
    
    @classmethod
    def math_symbol(cls, symbol, insert_text=None, parent=None):
        """Botón para un símbolo matemático"""
        btn = cls(symbol, parent=parent, object_name="mathSymbolButton")
        # ALmacena el texto a insertar como propiedad del botón
        btn.insert_text = insert_text if insert_text is not None else symbol
        return btn
    