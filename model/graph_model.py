import numpy as np

class GraphModel:
    def __init__(self, expression, x_range):
        self.expression = expression
        self.x_min, self.x_max = x_range

    def evaluate_function(self):
        x = np.linspace(self.x_min, self.x_max, 400)
        try:
            y = eval(self.expression, {"x": x, "np": np, "__builtins__": {}})
            return x, y
        except Exception as e:
            raise ValueError(f"Error evaluando la función: {e}")

    def evaluate_function_3d(self):
        x_vals = np.arange(self.x_min, self.x_max + 0.2, 0.2)
        y_vals = np.arange(self.x_min, self.x_max + 0.2, 0.2)  # usar el mismo rango por simplicidad
        X, Y = np.meshgrid(x_vals, y_vals)
        try:
            Z = eval(self.expression, {"x": X, "y": Y, "np": np, "__builtins__": {}})
            return X, Y, Z  
        except Exception as e:
            raise ValueError(f"Error evaluando la función 3D: {e}")