from sympy import symbols, diff, integrate, sympify

class SymCalModel:
    def __init__(self):
        self.x = symbols('x')
        self.y = symbols('y')
        self.history = []

    def derive(self, expression: str):
        f = sympify(expression)
        result = diff(f, self.x)
        self.history.append(("Derivada", expression, result))
        return result

    def integrate(self, expression: str, limits=None):
        f = sympify(expression)
        if limits:
            result = integrate(f, (self.x, *limits))
        else:
            result = integrate(f, self.x)
        self.history.append(("Integral", expression, result, limits))
        return result

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()
