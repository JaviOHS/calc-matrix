from model.vector_model import Vector

class VectorManager:
    def __init__(self):
        self.vectors = []
    
    def add_vector(self, vector):
        if isinstance(vector, Vector):
            self.vectors.append(vector)
        else:
            raise ValueError("El objeto agregado no es un vector válido.")
    
    def clear(self):
        self.vectors.clear()
        
    def get_vectors(self):
        return self.vectors

    def validate_vectors(self):
        for vector in self.vectors:
            vector.validate()
