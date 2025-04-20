from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class GraphController:
    def __init__(self, manager):
        self.manager = manager

    def generate_canvas_2d(self, inputs):
        try:
            expression = inputs["expression"]
            x_range = inputs["x_range"]
            
            if not expression or not x_range:
                raise ValueError("Expresión o rango no proporcionado")
                
            self.manager.create_model(expression, x_range)
            model = self.manager.get_model()
            
            x, y = model.evaluate_function()
            
            fig, ax = plt.subplots()
            ax.plot(x, y, label=f'f(x) = {expression}')
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.set_title("Gráfica 2D de la función")
            ax.legend()
            
            canvas = FigureCanvas(fig)
            return canvas
            
        except Exception as e:
            print(f"Error al generar gráfica: {e}")
            return None
        
    def generate_canvas_3d(self, inputs):
        try:
            expression = inputs["expression"]
            x_range = inputs["x_range"]
            
            if not expression or not x_range:
                raise ValueError("Expresión o rango no proporcionado")
                
            self.manager.create_model(expression, x_range)
            model = self.manager.get_model()
            
            x, y, z = model.evaluate_function_3d()
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(x, y, z, cmap='viridis')
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_title("Gráfica 3D de la función")
            
            canvas = FigureCanvas(fig)
            return canvas
            
        except Exception as e:
            print(f"Error al generar gráfica 3D: {e}")
            return None