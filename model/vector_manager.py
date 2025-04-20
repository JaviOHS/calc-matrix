from model.vector_model import Vector

class VectorManager:
    def __init__(self):
        """Inicializa el gestor con una lista vacía de vectores."""
        self.vectors = []
    
    def add_vector(self, vector):
        """Agrega un vector al gestor y valida que sea un vector válido."""
        if isinstance(vector, Vector):
            self.vectors.append(vector)
        else:
            raise ValueError("El objeto agregado no es un vector válido.")
    
    def clear(self):
        """Limpia todos los vectores almacenados."""
        self.vectors.clear()
        
    def get_vectors(self):
        """Devuelve la lista de vectores almacenados."""
        return self.vectors


    def validate_vectors(self):
        """Valida que todos los vectores en el gestor sean válidos."""
        for vector in self.vectors:
            vector.validate()
