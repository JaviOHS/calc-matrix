import json
import os

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
    
    def _load_content(self):
        """Carga el contenido del JSON"""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            content_path = os.path.join(base_dir, "assets", "content", "pages_content.json")
            
            with open(content_path, 'r', encoding='utf-8') as file:
                self._content = json.load(file)
        except Exception as e:
            print(f"Error al cargar el contenido: {e}")
            self._content = {"home": {}} # Contenido mínimo de respaldo en caso de error
    
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
    