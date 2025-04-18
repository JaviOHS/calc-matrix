import numpy as np

class Polynomial:
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def __add__(self, other):
        return Polynomial(self._operate(other, lambda a, b: a + b))

    def __sub__(self, other):
        return Polynomial(self._operate(other, lambda a, b: a - b))

    def __mul__(self, other):
        res = [0]*(len(self.coeffs) + len(other.coeffs) - 1)
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                res[i + j] += a * b
        return Polynomial(res)

    def _operate(self, other, op):
        a = self.coeffs[:]
        b = other.coeffs[:]
        max_len = max(len(a), len(b))
        a = [0]*(max_len - len(a)) + a
        b = [0]*(max_len - len(b)) + b
        return [op(x, y) for x, y in zip(a, b)]

    def __repr__(self):
        return self.pretty()

    def pretty(self):
        terms = []
        grado = len(self.coeffs) - 1
        for i, coef in enumerate(self.coeffs):
            if coef == 0:
                continue
            exp = grado - i
            term = ''
            if coef < 0:
                term += '- '
                coef = -coef
            elif terms:
                term += '+ '
            if exp == 0:
                term += f'{coef}'
            elif exp == 1:
                term += f'{coef}x'
            else:
                term += f'{coef}x^{exp}'
            terms.append(term)
        return ' '.join(terms) if terms else '0'
    
    def roots(self):
        if not self.coeffs or all(c == 0 for c in self.coeffs):
            raise ValueError("Polinomio inválido.")
        return np.roots(self.coeffs)
