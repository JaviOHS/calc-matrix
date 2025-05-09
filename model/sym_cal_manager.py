from model.sym_cal_model import SymCalModel

class SymCalManager:
    def __init__(self):
        self.model = SymCalModel()

    def get_derivative(self, expression: str, var=None):
        return self.model.derive(expression, var)

    def get_integral(self, expression: str, limits=None, var=None, constant=0):
        return self.model.integrate(expression, limits, var, constant)
    
    def solve_differential_equation(self, equation, initial_condition=None, x_range=None):
        return self.model.solve_differential_equation(equation, initial_condition, x_range)

    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        return self.model.solve_ode_euler(equation, initial_condition, x_range, h)

    def get_history(self):
        return self.model.get_history()

    def clear(self):
        self.model.clear()
