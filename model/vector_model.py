import numpy as np

class Vector:
    def __init__(self, components):
        """Inicializa un vector con una lista de componentes."""
        self.components = np.array(components)
    
    def __str__(self):
        """Devuelve una representación en cadena del vector."""
        return f"[{' ,'.join(map(str, self.components))}]"
    
    def validate(self):
        """Valida si el vector es válido (no vacío y tiene al menos una componente)."""
        if len(self.components) == 0:
            raise ValueError("El vector no puede estar vacío.")
        return True

    def magnitude(self):
        """Calcula la magnitud del vector (norma)."""
        return np.linalg.norm(self.components)

    def dot(self, other):
        """Realiza el producto punto entre este vector y otro."""
        if len(self.components) != len(other.components):
            raise ValueError("Los vectores deben tener la misma dimensión para el producto punto.")
        return np.dot(self.components, other.components)

    def cross(self, other):
        """Realiza el producto cruzado entre dos vectores 3D."""
        if len(self.components) != 3 or len(other.components) != 3:
            raise ValueError("El producto cruzado solo es válido para vectores 3D.")
        return Vector(np.cross(self.components, other.components))
