import json
from .resources import resource_path
from utils.core.font_weight_manager import FontWeightManager

class ContentManager:
    """Gestor de contenido dinámico para las páginas de la aplicación"""
    _instance = None
    _content = None
    
    @classmethod
    def get_instance(cls):
        """Implementa patrón Singleton para acceso global"""
        if cls._instance is None:
            cls._instance = ContentManager()
        return cls._instance
    
    def __init__(self):
        """Carga el contenido desde el archivo JSON"""
        self._load_content()
    
    def _process_html_content(self, content):
        """Procesa las etiquetas HTML en el contenido"""
        if isinstance(content, str):
            font_weight = FontWeightManager.get_weight("emphasis")
            return content.replace("<b>", f"<b style='font-weight: {font_weight}'>")
        elif isinstance(content, dict):
            return {k: self._process_html_content(v) for k, v in content.items()}
        elif isinstance(content, list):
            return [self._process_html_content(item) for item in content]
        return content
    
    def _load_content(self):
        """Carga y procesa el contenido del JSON"""
        try:
            content_path = resource_path("assets/content/pages_content.json")
            
            with open(content_path, 'r', encoding='utf-8') as file:
                raw_content = json.load(file)
                # Procesar todo el contenido
                self._content = self._process_html_content(raw_content)
        except Exception as e:
            print(f"Error al cargar el contenido: {e}")
            self._content = {"home": {}}  # Contenido mínimo de respaldo en caso de error
    
    def get_page_content(self, page_key):
        """Obtiene el contenido para una página específica"""
        if not self._content or page_key not in self._content:
            return {}
        return self._content.get(page_key, {})
    
    def get_feature(self, page_key, feature_index):
        """Obtiene una característica específica de una página"""
        page = self.get_page_content(page_key)
        features = page.get("features", [])
        if 0 <= feature_index < len(features):
            return features[feature_index]
        return None
