from utils.core.figure_manager import FigureManager
from controller.plot_controller.plot_2d_controller import Plot2DController
from controller.plot_controller.plot_3d_controller import Plot3DController
from controller.plot_controller.plot_ode_controller import PlotODEController
from controller.plot_controller.plot_dis_controller import PlotDistributionController
from utils.layout.plot_style_helper import PlotStyleHelper

class GraphController:
    def __init__(self, manager):
        self.figure_manager = FigureManager()
        self.style_helper = PlotStyleHelper()
        
        self.plot_2d = Plot2DController(manager, self.figure_manager, self.style_helper)
        self.plot_3d = Plot3DController(manager, self.figure_manager, self.style_helper)
        self.plot_ode = PlotODEController(manager, self.figure_manager, self.style_helper)
        self.plot_distribution = PlotDistributionController(manager, self.figure_manager, self.style_helper)

    def execute_operation(self, operation_type, inputs):
        """Método fachada para dirigir las operaciones a los controladores especializados"""
        operations = {
            "2d_graph": self.plot_2d.generate_canvas,
            "3d_graph": self.plot_3d.generate_canvas,
            "ode_solution": self.plot_ode.generate_solution_canvas,
            "ode_comparison": self.plot_ode.generate_comparison_canvas,
            "distribution": self.plot_distribution.create_epidemic_plot
        }

        if operation_type not in operations:
            raise ValueError(f"Tipo de operación no soportado: {operation_type}")

        return operations[operation_type](inputs)

    def generate_ode_solution_canvas(self, equation, solution_points, initial_condition=None, x_range=None, is_numerical=True):
        """Fachada para generar gráficos de soluciones de EDOs"""
        return self.plot_ode.generate_solution_canvas(equation=equation,solution_points=solution_points,initial_condition=initial_condition,x_range=x_range, is_numerical=is_numerical)

    def generate_ode_comparison_canvas(self, equation, solutions, initial_condition=None, x_range=None, h=0.1, method_names=None):
        """Fachada para generar gráficos comparativos de métodos numéricos"""
        return self.plot_ode.generate_comparison_canvas(equation=equation,solutions=solutions,initial_condition=initial_condition,x_range=x_range,h=h)
    
    def create_epidemic_plot(self, times, susceptible, infected, recovered, params):
        """Fachada para crear un gráfico de epidemia"""
        return self.plot_distribution.create_epidemic_plot(times=times,susceptible=susceptible,infected=infected,recovered=recovered,params=params)