from model.sym_cal_model import SymCalModel

class SymCalManager:
    def __init__(self):
        self.model = SymCalModel()

    def get_derivative(self, expression: str):
        return self.model.derive(expression)

    def get_integral(self, expression: str, limits=None):
        return self.model.integrate(expression, limits)

    def get_history(self):
        return self.model.get_history()

    def clear(self):
        self.model.clear()

