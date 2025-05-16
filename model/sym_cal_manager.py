from model.sym_cal_model import SymCalModel

class SymCalManager:
    def __init__(self):
        self.model = SymCalModel()

    def get_derivative(self, expression: str, var=None):
        return self.model.derive(expression, var)

    def get_integral(self, expression, limits=None, var=None, constant=0):
        return self.model.integrate(expression, limits, var, constant)
    
    def solve_differential_equation(self, equation, initial_condition=None, x_range=None):
        return self.model.solve_differential_equation(equation, initial_condition, x_range)

    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        return self.model.solve_ode_euler(equation, initial_condition, x_range, h)

    def solve_ode_heun(self, equation, initial_condition, x_range, h=0.1):
        return self.model.solve_ode_heun(equation, initial_condition, x_range, h)

    def solve_ode_rk4(self, equation, initial_condition, x_range, h=0.1):
        return self.model.solve_ode_rk4(equation, initial_condition, x_range, h)
    
    def solve_ode_taylor(self, equation, initial_condition, x_range, h=0.1):
        return self.model.solve_ode_taylor(equation, initial_condition, x_range, h)

    def solve_ode_numerical(self, equation, initial_condition, x_range, h=0.1, method="euler"):
        """Método genérico para llamar a los métodos numéricos de resolución de EDOs"""
        method_func = getattr(self.model, f"solve_ode_{method}", None)
        if not method_func:
            raise ValueError(f"Método numérico desconocido: {method}")
        
        return method_func(equation, initial_condition, x_range, h)
    
    def clear(self):
        """Limpia el modelo y los datos internos"""
        self.model.clear()