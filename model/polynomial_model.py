import sympy as sp

class Polynomial:
    def __init__(self, coeffs, var='x'):
        self.var = var
        x = sp.Symbol(var)
        self.poly = sp.Poly.from_list(coeffs, gens=(x,), domain='QQ')
        self.coefficients = coeffs

    def __repr__(self):
        return str(self.poly.as_expr())

    def divide(self, other):
        quotient, remainder = sp.div(self.poly, other.poly)
        return Polynomial(quotient.all_coeffs()), Polynomial(remainder.all_coeffs())

    def evaluate(self, x_val):
        return self.poly.eval(x_val)

    def integral(self, constant=0):
        x = sp.Symbol(self.var)
        expr = self.to_sympy_expr()
        integrated_expr = sp.integrate(expr, x) + constant  # Integración + constante
        # Simplificar y convertir a un formato más legible
        # Elimina el uso de 'simplify' que genera una fracción no deseada
        integrated_expr = sp.expand(integrated_expr)  # Expandir para evitar fracciones complejas
        return Polynomial([c for c in sp.Poly(integrated_expr, x).all_coeffs()])

    def derivative(self):
        expr = self.to_sympy_expr()
        x = sp.Symbol(self.var)
        derived_expr = sp.diff(expr, x)  # Derivada del polinomio
        coeffs = sp.Poly(derived_expr, x).all_coeffs()  # Coeficientes de la derivada
        return Polynomial(coeffs)

    def to_sympy_expr(self):
        x = sp.Symbol(self.var)
        return sum(c * x**i for i, c in enumerate(reversed(self.coefficients)))

    def get_roots(self):
        x = sp.Symbol(self.var)
        expr = self.to_sympy_expr()
        return sp.solve(expr, x)
