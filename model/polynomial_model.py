import sympy as sp

class Polynomial:
    def __init__(self, coeffs, var='x'):
        self.var = var
        x = sp.Symbol(var)
        self.poly = sp.Poly.from_list(coeffs, gens=(x,), domain='QQ')
        self.coefficients = coeffs

    def __repr__(self):
        return str(self.poly.as_expr())

    def derivative(self):
        from model.sym_cal_model import SymCalModel
        calc = SymCalModel()
        return calc.derive(self.coefficients, var=self.var)

    def integral(self, constant=0):
        from model.sym_cal_model import SymCalModel
        calc = SymCalModel()
        return calc.integrate(self.coefficients, var=self.var, constant=constant)

    def evaluate(self, x_val):
        return self.poly.eval(x_val)

    def to_sympy_expr(self):
        x = sp.Symbol(self.var)
        return sum(c * x**i for i, c in enumerate(reversed(self.coefficients)))

    def get_roots(self):
        x = sp.Symbol(self.var)
        expr = self.to_sympy_expr()
        return sp.solve(expr, x)
